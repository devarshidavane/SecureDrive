# Secure Drive

Secure Drive is a Windows desktop antivirus-style application built with PySide6.

## Project Structure

- App entry point: `main.py`
- Main window/controller: `securedrive.py`
- Active generated UI module: `ui_secureDrive.py`
- Source Qt Designer file for the active UI: `secureDrive.ui`
- Resource bundle source: `resources.qrc`
- Generated resource module: `resources_rc.py`
- Real-time scanner: `Scans/Real_time_scan.py`
- Shared scan engine: `Scans/scanner.py`
- Full-scan entry point: `Scans/full_scan.py`
- Signature updater: `Scans/database.py`
- Malware hash database: `Malware Hash Database/hashes.db`

`secureDrive_ui.py` and `secure Drive.ui` are older/alternate UI outputs and are not imported by the app entry point.

## Setup

Create or refresh a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the app:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Notes

- The real-time scanner watches the user's Desktop and Downloads folders.
- Detected files are moved into `Quarantine/`.
- Threat detections are appended to `threat_log.txt`.
- Full scans and signature updates run in background Qt processes.
- Backend progress and completion messages appear on the Notifications page.
