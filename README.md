# Secure Drive

Secure Drive is a Windows desktop antivirus-style application built with PySide6.

## Current Phase 1 Baseline

- App entry point: `main.py`
- Main window/controller: `securedrive.py`
- Active generated UI module: `ui_secureDrive.py`
- Source Qt Designer file for the active UI: `secureDrive.ui`
- Resource bundle source: `resources.qrc`
- Generated resource module: `resources_rc.py`
- Real-time scanner: `Scans/Real_time_scan.py`
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
- Full scan and database update integration are intentionally left for later phases.
