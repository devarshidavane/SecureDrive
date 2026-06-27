import concurrent.futures
import hashlib
import os
import shutil
import sqlite3
import time
import uuid
import requests
from pathlib import Path

import psutil
from pybloom_live import BloomFilter
from winotify import Notification, audio  # type: ignore

from paths import APP_ICON_PATH, HASH_DB_PATH, QUARANTINE_DIR, THREAT_LOG_PATH

SERVER_URL = "http://127.0.0.1:8000"
BLOOM_FILTER_PATH = Path(__file__).parent / "threats.bloom"
HASH_TABLES = ("md5", "sha1", "sha256")
READ_CHUNK_SIZE = 8192
PROGRESS_INTERVAL = 500
MAX_FILE_SIZE_BYTES = 500 * 1024 * 1024  # Skip files larger than 500MB to prevent DoS


def hash_file(file_path):
    path = Path(file_path)
    try:
        if path.stat().st_size > MAX_FILE_SIZE_BYTES:
            print(f"[SecureDrive] Skipping {path}: Exceeds maximum size limit.")
            return None
    except OSError:
        return None

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


def get_bloom_filter():
    if not BLOOM_FILTER_PATH.exists():
        print("[SecureDrive] Downloading Bloom Filter from server...")
        try:
            resp = requests.get(f"{SERVER_URL}/bloom_filter")
            if resp.status_code == 200:
                with open(BLOOM_FILTER_PATH, "wb") as f:
                    f.write(resp.content)
            else:
                print("[SecureDrive] Failed to fetch Bloom Filter.")
                return None
        except Exception as e:
            print(f"[SecureDrive] Server offline. {e}")
            return None
    
    try:
        with open(BLOOM_FILTER_PATH, "rb") as f:
            return BloomFilter.fromfile(f)
    except Exception as e:
        print(f"[SecureDrive] Error loading Bloom Filter: {e}")
        return None

def check_bloom_filter(hashes, bloom):
    if bloom is None:
        return None
    
    # We use SHA-256 in the bloom filter
    hash_value = hashes.get("sha256")
    if hash_value and hash_value in bloom:
        return "sha256", hash_value
        
    return None


def log_threat(source_path, quarantine_path, hash_type=None, hash_value=None):
    THREAT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    write_header = not THREAT_LOG_PATH.exists() or THREAT_LOG_PATH.stat().st_size == 0
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    htype = str(hash_type) if hash_type else "N/A"
    hval = str(hash_value) if hash_value else "N/A"
    
    with THREAT_LOG_PATH.open("a", encoding="utf-8") as log_handle:
        if write_header:
            log_handle.write(
                f"{'TIMESTAMP'.ljust(20)} | {'HASH TYPE'.ljust(10)} | {'HASH VALUE'.ljust(64)} | {'ORIGINAL PATH'.ljust(80)} | {'QUARANTINE PATH'}\n"
            )
            log_handle.write("-" * 200 + "\n")
            
        log_handle.write(
            f"{timestamp.ljust(20)} | {htype.ljust(10)} | {hval.ljust(64)} | {str(source_path).ljust(80)} | {str(quarantine_path)}\n"
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
    destination = QUARANTINE_DIR / f"{uuid.uuid4()}_{source.name}.locked"

    try:
        shutil.move(str(source), str(destination))
        # Future improvement: XOR encode the file contents here to completely disarm it.
    except OSError as exc:
        print(f"[SecureDrive] Quarantine error for {source}: {exc}")
        return None

    hash_type, hash_value = match if match else (None, None)
    log_threat(source, destination, hash_type, hash_value)
    notify_user(source.name)
    print(f"[SecureDrive] Threat quarantined: {source.name}")
    return destination


def scan_file(file_path, quarantine=True, bloom=None):
    if bloom is None:
        bloom = get_bloom_filter()
        
    # Pipeline Step 1: Hash-based signature matching (Bloom Filter)
    hashes = hash_file(file_path)
    if hashes:
        match = check_bloom_filter(hashes, bloom)
        if match:
            print(f"[SecureDrive] Signature threat match found in {file_path}")
            if quarantine:
                quarantine_file(file_path, match)
            return True

    # Pipeline Step 2: Dynamic Deep Scan (Sandbox Detonation)
    # For demonstration, we'll assume any unknown .exe is 'suspicious' and detonated.
    # In a real scenario, this would be gated by a lightweight heuristic check.
    if file_path.suffix.lower() in [".exe", ".bat"]:
        print(f"[SecureDrive] Suspicious executable {file_path.name} found. Detonating in Sandbox...")
        try:
            from sandbox_wrapper import detonate_in_sandbox
            success, log_output = detonate_in_sandbox(file_path)
            print(f"[SecureDrive] Sandbox Log for {file_path.name}:\n{log_output}")
            
            # If the log output shows bad behavior, we could quarantine here
            # if "Malicious Behavior Detected" in log_output:
            #     if quarantine:
            #         quarantine_file(file_path)
            #     return True
        except ImportError:
            pass

    # Pipeline Step 3: Future Low-parameter ML Model
    # if ml_model_predict(file_path):
    #     ...

    return False


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


def run_full_scan(root_dirs=None, max_workers=None):
    if max_workers is None:
        try:
            from system_profiler import get_optimal_thread_count
            max_workers = get_optimal_thread_count()
        except ImportError:
            max_workers = 8

    roots = root_dirs or get_all_drives()
    roots = [Path(root) for root in roots if Path(root).exists()]
    print(
        f"[SecureDrive] Full scan starting across {len(roots)} drive(s) with {max_workers} threads.",
        flush=True,
    )

    scanned = 0
    threats = 0
    max_pending = max_workers * 4

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        pending = set()
        bloom = get_bloom_filter()
        for root in roots:
            try:
                for file_path in iter_files(root):
                    pending.add(executor.submit(scan_file, file_path, True, bloom))
                    if len(pending) < max_pending:
                        continue

                    done, pending = concurrent.futures.wait(
                        pending,
                        return_when=concurrent.futures.FIRST_COMPLETED,
                    )
                    for future in done:
                        scanned += 1
                        try:
                            if future.result():
                                threats += 1
                        except Exception as exc:
                            print(f"[SecureDrive] Scan worker error: {exc}", flush=True)

                        if scanned % PROGRESS_INTERVAL == 0:
                            print(
                                f"[SecureDrive] Scan progress: {scanned} files; "
                                f"{threats} threat(s).",
                                flush=True,
                            )
            except OSError as exc:
                print(f"[SecureDrive] Error walking {root}: {exc}", flush=True)

        for future in concurrent.futures.as_completed(pending):
            scanned += 1
            try:
                if future.result():
                    threats += 1
            except Exception as exc:
                print(f"[SecureDrive] Scan worker error: {exc}", flush=True)

            if scanned % PROGRESS_INTERVAL == 0:
                print(
                    f"[SecureDrive] Scan progress: {scanned} files; "
                    f"{threats} threat(s).",
                    flush=True,
                )

    print(
        f"[SecureDrive] Full scan complete. Files scanned: {scanned}. "
        f"Threats: {threats}.",
        flush=True,
    )
    return scanned, threats
