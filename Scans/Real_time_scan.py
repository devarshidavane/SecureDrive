import hashlib
import os
import shutil
import sqlite3
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

import psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from winotify import Notification, audio  # type: ignore

from paths import APP_ICON_PATH, HASH_DB_PATH, QUARANTINE_DIR, THREAT_LOG_PATH

# ==============================
# PATH SETUP
# ==============================

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

logo_path = str(APP_ICON_PATH)
db_path = str(HASH_DB_PATH)
quarantine_folder = str(QUARANTINE_DIR)

# ==============================
# CONFIG
# ==============================

WATCH_PATHS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
]

# Scan common malware delivery targets to reduce CPU overhead.
MONITORED_EXTENSIONS = {
    ".exe", ".dll", ".msi", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".js",
    ".jar", ".com", ".pif", ".lnk", ".zip", ".rar", ".7z", ".iso", ".img",
    ".docm", ".xlsm", ".pptm", ".pdf", ".py", ".pyw", ".apk",
}

SKIP_SUFFIXES = {".tmp", ".part", ".crdownload", ".download"}
MAX_FILE_SIZE_BYTES = 250 * 1024 * 1024

executor = ThreadPoolExecutor(max_workers=4)
recent_files = {}
recent_lock = threading.Lock()
DEDUP_WINDOW_SECONDS = 3


# ==============================
# SINGLE INSTANCE GUARD
# ==============================

def find_existing_instance():
    current_pid = os.getpid()
    current_script = os.path.normcase(os.path.abspath(__file__))

    for proc in psutil.process_iter(["pid", "cmdline"]):
        try:
            if proc.info["pid"] == current_pid:
                continue

            cmdline = proc.info.get("cmdline") or []
            normalized_cmdline = [
                os.path.normcase(os.path.abspath(part))
                for part in cmdline
                if isinstance(part, str) and part
            ]

            if current_script in normalized_cmdline:
                return proc.info["pid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return None


# ==============================
# FILE FILTERS
# ==============================

def should_scan_file(file_path):
    if not os.path.isfile(file_path):
        return False

    lowered = file_path.lower()
    for suffix in SKIP_SUFFIXES:
        if lowered.endswith(suffix):
            return False

    extension = os.path.splitext(lowered)[1]
    if extension and extension not in MONITORED_EXTENSIONS:
        return False

    try:
        if os.path.getsize(file_path) > MAX_FILE_SIZE_BYTES:
            return False
    except OSError:
        return False

    return True


def should_process_event(file_path):
    now = time.time()
    with recent_lock:
        last_time = recent_files.get(file_path)
        if last_time and (now - last_time) < DEDUP_WINDOW_SECONDS:
            return False

        recent_files[file_path] = now

        stale = [p for p, ts in recent_files.items() if (now - ts) > (DEDUP_WINDOW_SECONDS * 3)]
        for path in stale:
            recent_files.pop(path, None)

    return True


# ==============================
# FILE HANDLER
# ==============================

class NewFileHandler(FileSystemEventHandler):
    def _submit_if_needed(self, path):
        if not should_process_event(path):
            return
        if not should_scan_file(path):
            return

        print(f"[+] New candidate file detected: {path}")
        executor.submit(process_file, path)

    def on_created(self, event):
        if not event.is_directory:
            self._submit_if_needed(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._submit_if_needed(event.dest_path)


# ==============================
# SCAN LOGIC
# ==============================

def process_file(file_path):
    time.sleep(1.5)
    hashes = get_file_hashes(file_path)
    if hashes:
        check_hashes_in_db(file_path, hashes)


# ==============================
# HASHING
# ==============================

def get_file_hashes(file_path):
    hashes = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
    }

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                for hash_builder in hashes.values():
                    hash_builder.update(chunk)
    except (FileNotFoundError, PermissionError, OSError):
        return None

    return {name: hash_builder.hexdigest() for name, hash_builder in hashes.items()}


# ==============================
# DATABASE CHECK
# ==============================

def check_hashes_in_db(file_path, hashes):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for hash_type, hash_value in hashes.items():
                if hash_type not in {"md5", "sha1", "sha256"}:
                    continue
                cursor.execute(f"SELECT 1 FROM {hash_type} WHERE hash = ? LIMIT 1", (hash_value,))
                if cursor.fetchone():
                    quarantine_file(file_path)
                    break
    except Exception as e:
        print(f"[DB ERROR] {e}")


# ==============================
# QUARANTINE
# ==============================

def quarantine_file(file_path):
    try:
        if not os.path.exists(quarantine_folder):
            os.makedirs(quarantine_folder)

        file_name = os.path.basename(file_path)
        new_name = f"{uuid.uuid4()}_{file_name}"
        new_path = os.path.join(quarantine_folder, new_name)

        shutil.move(file_path, new_path)
        log_threat(file_path)
        notify_user(file_name)

        print(f"[!] Threat quarantined: {file_name}")
    except Exception as e:
        print(f"[QUARANTINE ERROR] {e}")


# ==============================
# NOTIFICATION
# ==============================

def notify_user(file_name):
    try:
        toast = Notification(
            app_id="Secure Drive",
            title="Virus Detected",
            msg=f"{file_name} moved to quarantine.",
            icon=logo_path,
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except Exception as e:
        print(f"[NOTIFY ERROR] {e}")


# ==============================
# THREAT LOG
# ==============================

def log_threat(file_path):
    with open(THREAT_LOG_PATH, "a", encoding="utf-8") as log_handle:
        log_handle.write(f"{time.ctime()} - Threat detected: {file_path}\n")


# ==============================
# MAIN SERVICE
# ==============================

def start_realtime_protection():
    observer = Observer()
    handler = NewFileHandler()

    valid_paths = [path for path in WATCH_PATHS if os.path.isdir(path)]
    if not valid_paths:
        print("[ERROR] No valid watch paths found.")
        return

    for path in valid_paths:
        observer.schedule(handler, path, recursive=True)
        print(f"[WATCHING] {path}")

    observer.start()
    print("[SecureDrive] Real-time protection running in background.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()


if __name__ == "__main__":
    existing_pid = find_existing_instance()
    if existing_pid:
        print(f"[SecureDrive] Real-time scanner already running (PID: {existing_pid}).")
        sys.exit(0)

    start_realtime_protection()
