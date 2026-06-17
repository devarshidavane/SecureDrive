import concurrent.futures
import hashlib
import os
import shutil
import sqlite3
import time
import uuid
from pathlib import Path

import psutil
from winotify import Notification, audio  # type: ignore

from paths import APP_ICON_PATH, HASH_DB_PATH, QUARANTINE_DIR, THREAT_LOG_PATH


HASH_TABLES = ("md5", "sha1", "sha256")
READ_CHUNK_SIZE = 8192


def hash_file(file_path):
    path = Path(file_path)
    hashes = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
    }

    try:
        with path.open("rb") as file:
            while chunk := file.read(READ_CHUNK_SIZE):
                for hash_builder in hashes.values():
                    hash_builder.update(chunk)
    except (FileNotFoundError, PermissionError, OSError) as exc:
        print(f"[SecureDrive] Could not read {path}: {exc}")
        return None

    return {name: hash_builder.hexdigest() for name, hash_builder in hashes.items()}


def find_matching_hash(hashes):
    if not HASH_DB_PATH.exists():
        raise FileNotFoundError(f"Malware hash database not found: {HASH_DB_PATH}")

    with sqlite3.connect(HASH_DB_PATH) as conn:
        cursor = conn.cursor()
        for table in HASH_TABLES:
            hash_value = hashes.get(table)
            if not hash_value:
                continue

            cursor.execute(
                f"SELECT 1 FROM {table} WHERE hash = ? LIMIT 1",
                (hash_value,),
            )
            if cursor.fetchone():
                return table, hash_value

    return None


def log_threat(source_path, quarantine_path, hash_type=None, hash_value=None):
    THREAT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    hash_detail = f" [{hash_type}: {hash_value}]" if hash_type and hash_value else ""
    with THREAT_LOG_PATH.open("a", encoding="utf-8") as log_handle:
        log_handle.write(
            f"{timestamp} - Threat detected{hash_detail}: {source_path} -> {quarantine_path}\n"
        )


def notify_user(file_name):
    try:
        toast = Notification(
            app_id="Secure Drive",
            title="Virus Detected",
            msg=f"{file_name} moved to quarantine.",
            icon=str(APP_ICON_PATH),
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except Exception as exc:
        print(f"[SecureDrive] Notification error: {exc}")


def quarantine_file(file_path, match=None):
    source = Path(file_path)
    if not source.exists():
        print(f"[SecureDrive] Cannot quarantine missing file: {source}")
        return None

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    destination = QUARANTINE_DIR / f"{uuid.uuid4()}_{source.name}"

    try:
        shutil.move(str(source), str(destination))
    except OSError as exc:
        print(f"[SecureDrive] Quarantine error for {source}: {exc}")
        return None

    hash_type, hash_value = match if match else (None, None)
    log_threat(source, destination, hash_type, hash_value)
    notify_user(source.name)
    print(f"[SecureDrive] Threat quarantined: {source.name}")
    return destination


def scan_file(file_path, quarantine=True):
    hashes = hash_file(file_path)
    if not hashes:
        return False

    match = find_matching_hash(hashes)
    if not match:
        return False

    print(f"[SecureDrive] Threat match found in {file_path}")
    if quarantine:
        quarantine_file(file_path, match)
    return True


def iter_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            yield Path(dirpath) / filename


def get_all_drives():
    return [
        partition.device
        for partition in psutil.disk_partitions()
        if partition.fstype
    ]


def run_full_scan(root_dirs=None, max_workers=8):
    roots = root_dirs or get_all_drives()
    roots = [Path(root) for root in roots if Path(root).exists()]
    print(f"[SecureDrive] Full scan starting across {len(roots)} drive(s).")

    scanned = 0
    threats = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root in roots:
            try:
                for file_path in iter_files(root):
                    futures.append(executor.submit(scan_file, file_path))
            except OSError as exc:
                print(f"[SecureDrive] Error walking {root}: {exc}")

        for future in concurrent.futures.as_completed(futures):
            scanned += 1
            try:
                if future.result():
                    threats += 1
            except Exception as exc:
                print(f"[SecureDrive] Scan worker error: {exc}")

    print(f"[SecureDrive] Full scan complete. Files scanned: {scanned}. Threats: {threats}.")
    return scanned, threats

