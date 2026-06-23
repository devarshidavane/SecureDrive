import os
import sqlite3
import time
from pathlib import Path

import requests

from paths import HASH_DB_DIR, HASH_DB_PATH


BASE_URLS = {
    "md5": "https://raw.githubusercontent.com/aaryanrlondhe/Malware-Hash-Database/main/MD5/md5_hashes_",
    "sha1": "https://raw.githubusercontent.com/aaryanrlondhe/Malware-Hash-Database/main/SHA1/sha1_hashes_",
    "sha256": "https://raw.githubusercontent.com/aaryanrlondhe/Malware-Hash-Database/main/SHA256/sha256_hashes_",
}


def fetch_and_save_file(url, directory, filename, timeout=30):
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / filename

    if file_path.exists():
        return file_path

    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 404:
            return None
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Download failed for {url}: {exc}") from exc

    file_path.write_text(response.text, encoding="utf-8")
    return file_path


def download_hash_files(base_url, prefix):
    files = []
    index = 1

    while True:
        url = f"{base_url}{index}.txt"
        filename = f"{prefix}_hashes_{index}.txt"
        file_path = fetch_and_save_file(url, HASH_DB_DIR, filename)
        if file_path is None:
            break

        files.append(file_path)
        index += 1

    return files


def create_database():
    HASH_DB_DIR.mkdir(parents=True, exist_ok=True)
    temporary_path = HASH_DB_PATH.with_suffix(".db.tmp")
    if temporary_path.exists():
        temporary_path.unlink()

    conn = sqlite3.connect(temporary_path)
    cursor = conn.cursor()
    for table in BASE_URLS:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (hash TEXT PRIMARY KEY)")
    conn.commit()
    return conn, temporary_path


def insert_hashes(conn, table, files):
    cursor = conn.cursor()
    inserted = 0

    for file_path in files:
        with Path(file_path).open("r", encoding="utf-8", errors="ignore") as file:
            rows = [(line.strip(),) for line in file if line.strip()]

        cursor.executemany(
            f"INSERT OR IGNORE INTO {table} (hash) VALUES (?)",
            rows,
        )
        inserted += len(rows)

    conn.commit()
    return inserted


def update_database():
    print("[SecureDrive] Updating antivirus signatures...", flush=True)
    downloaded_files = {}

    for prefix, base_url in BASE_URLS.items():
        print(
            f"[SecureDrive] Downloading {prefix.upper()} hash files...",
            flush=True,
        )
        downloaded_files[prefix] = download_hash_files(base_url, prefix)

    missing_sets = [
        prefix.upper()
        for prefix, files in downloaded_files.items()
        if not files
    ]
    if missing_sets:
        missing = ", ".join(missing_sets)
        raise RuntimeError(
            f"Signature update incomplete; no files available for: {missing}. "
            "The existing database was preserved."
        )

    conn, temporary_path = create_database()
    try:
        for prefix, files in downloaded_files.items():
            inserted = insert_hashes(conn, prefix, files)
            print(
                f"[SecureDrive] Loaded {inserted} {prefix.upper()} hashes.",
                flush=True,
            )
    finally:
        conn.close()

    os.replace(temporary_path, HASH_DB_PATH)
    print(
        "[SecureDrive] Antivirus signatures updated successfully.",
        flush=True,
    )
    time.sleep(1)


if __name__ == "__main__":
    update_database()
