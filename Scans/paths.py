from pathlib import Path


SCANS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCANS_DIR.parent

HASH_DB_DIR = PROJECT_ROOT / "Malware Hash Database"
HASH_DB_PATH = HASH_DB_DIR / "hashes.db"

QUARANTINE_DIR = PROJECT_ROOT / "Quarantine"
THREAT_LOG_PATH = PROJECT_ROOT / "threat_log.txt"

APP_ICON_PATH = PROJECT_ROOT / "icons" / "Logo - Secure Drive.png"

