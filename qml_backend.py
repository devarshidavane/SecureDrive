import os
import sys
import hashlib
import requests
import json
import urllib.request
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Property, Signal, QProcess
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QLineEdit, QApplication

class SecureDriveBackend(QObject):
    backendStatusChanged = Signal()
    realtimeEnabledChanged = Signal()
    threatsBlockedChanged = Signal()

    def __init__(self, project_root):
        super().__init__()
        self._project_root = str(project_root)
        self.scans_dir = project_root / "Scans"
        self.realtime_script_path = str(self.scans_dir / "Real_time_scan.py")
        self.full_scan_script_path = str(self.scans_dir / "full_scan.py")
        self.database_update_script_path = str(self.scans_dir / "database.py")
        self.session_file = project_root / "session.json"
        
        self._backend_status = "System running normally."
        self._realtime_enabled = False
        self._threats_blocked = "0"
        
        # Load session data
        if self.session_file.exists():
            try:
                with open(self.session_file, "r") as f:
                    data = json.load(f)
                    self._backend_status = data.get("backend_status", self._backend_status)
                    self._threats_blocked = data.get("threats_blocked", self._threats_blocked)
            except Exception as e:
                print(f"Error loading session: {e}")
        
        self.active_processes = {}
        
        # Determine initial realtime state
        import psutil
        target_script = os.path.normcase(os.path.abspath(self.realtime_script_path))
        for proc in psutil.process_iter(["pid", "cmdline"]):
            try:
                cmdline = proc.info.get("cmdline") or []
                normalized_cmdline = [os.path.normcase(os.path.abspath(part)) for part in cmdline if isinstance(part, str)]
                if target_script in normalized_cmdline:
                    self._realtime_enabled = True
                    break
            except Exception:
                pass

    def _save_session(self):
        try:
            with open(self.session_file, "w") as f:
                json.dump({
                    "backend_status": self._backend_status,
                    "threats_blocked": self._threats_blocked,
                }, f)
        except Exception as e:
            print(f"Error saving session: {e}")

    @Property(str, notify=backendStatusChanged)
    def backend_status(self):
        return self._backend_status

    def set_backend_status(self, val):
        self._backend_status = val
        self.backendStatusChanged.emit()
        self._save_session()
        print(f"[UI Status] {val}")

    @Property(bool, notify=realtimeEnabledChanged)
    def realtime_enabled(self):
        return self._realtime_enabled

    def set_realtime_enabled(self, val):
        self._realtime_enabled = val
        self.realtimeEnabledChanged.emit()

    @Property(str, notify=threatsBlockedChanged)
    def threats_blocked(self):
        return self._threats_blocked

    @Property(str, constant=True)
    def project_root(self):
        return self._project_root.replace("\\", "/")

    @Slot(bool)
    def toggle_realtime(self, enable):
        import subprocess
        if enable:
            try:
                # 0x00000008 = DETACHED_PROCESS, 0x00000200 = CREATE_NEW_PROCESS_GROUP
                creationflags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
                subprocess.Popen([sys.executable, self.realtime_script_path], creationflags=creationflags, close_fds=True)
                self.set_realtime_enabled(True)
                self.set_backend_status("Real-time protection started.")
            except Exception as e:
                self.set_backend_status(f"Error starting protection: {e}")
                self.set_realtime_enabled(False)
        else:
            import psutil
            target_script = os.path.normcase(os.path.abspath(self.realtime_script_path))
            for proc in psutil.process_iter(["pid", "cmdline"]):
                try:
                    cmdline = proc.info.get("cmdline") or []
                    if target_script in [os.path.normcase(os.path.abspath(part)) for part in cmdline if isinstance(part, str)]:
                        proc.kill()
                except Exception:
                    pass
            self.set_realtime_enabled(False)
            self.set_backend_status("Real-time protection stopped.")

    def _start_process(self, script_path, name):
        if name in self.active_processes:
            self.set_backend_status(f"{name} is already running.")
            return

        process = QProcess(self)
        process.setProgram(sys.executable)
        process.setArguments(["-u", script_path])
        process.setWorkingDirectory(self._project_root)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        
        process.readyReadStandardOutput.connect(lambda: self.set_backend_status(bytes(process.readAllStandardOutput()).decode().strip() or self._backend_status))
        process.finished.connect(lambda code, status: self.active_processes.pop(name, None))
        
        self.active_processes[name] = process
        process.start()
        self.set_backend_status(f"{name} started.")

    @Slot()
    def start_full_scan(self):
        self._start_process(self.full_scan_script_path, "Full System Scan")

    @Slot()
    def start_database_update(self):
        self._start_process(self.database_update_script_path, "Database Update")

    @Slot(str)
    def scan_specific_file(self, file_url):
        file_path = urllib.request.url2pathname(file_url.replace('file:///', ''))
        # On Windows, url2pathname might prepend an extra slash or keep it if file:///C:/.. -> C:/..
        if file_path.startswith('/') and ':' in file_path:
            file_path = file_path[1:]

        if str(self.scans_dir) not in sys.path:
            sys.path.append(str(self.scans_dir))
        try:
            from scanner import scan_file
            self.set_backend_status(f"Scanning {file_path}")
            QApplication.processEvents()
            
            is_threat = scan_file(file_path, quarantine=True)
            if is_threat:
                try:
                    count = int(self._threats_blocked)
                    self._threats_blocked = str(count + 1)
                    self.threatsBlockedChanged.emit()
                    self._save_session()
                except:
                    pass
                self.set_backend_status("File scan complete: Threat found.")
            else:
                self.set_backend_status("File scan complete: Clean.")
        except Exception as e:
            self.set_backend_status(f"Scan error: {e}")

    @Slot()
    def check_password_breach(self):
        from PySide6.QtWidgets import QWidget
        parent = QWidget()
        parent.setAttribute(parent.WindowAttribute.WA_DontShowOnScreen)
        password, ok = QInputDialog.getText(parent, "Password Check", "Enter password:", QLineEdit.Password)
        if ok and password:
            sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            try:
                resp = requests.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}")
                if resp.status_code == 200:
                    for line in resp.text.splitlines():
                        if line.split(':')[0] == sha1[5:]:
                            QMessageBox.warning(parent, "Breached", f"Password found {line.split(':')[1]} times!")
                            return
                    QMessageBox.information(parent, "Safe", "Password is safe.")
            except Exception as e:
                QMessageBox.critical(parent, "Error", str(e))

    @Slot()
    def check_email_breach(self):
        from PySide6.QtWidgets import QWidget
        parent = QWidget()
        parent.setAttribute(parent.WindowAttribute.WA_DontShowOnScreen)
        email, ok = QInputDialog.getText(parent, "Email Check", "Enter email:")
        if ok and email:
            QMessageBox.information(parent, "API Key Required", "The HIBP Email API requires a paid key.")
            
    @Slot(result=str)
    def get_threat_logs(self):
        log_path = Path(self._project_root) / "threat_log.txt"
        if not log_path.exists():
            return "No threats logged yet."
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading log: {e}"
            
    @Slot(result=str)
    def get_quarantined_files(self):
        import datetime
        quarantine_dir = Path(self._project_root) / "Quarantine"
        if not quarantine_dir.exists():
            return "[]"
        
        files_data = []
        try:
            for item in quarantine_dir.iterdir():
                if item.is_file():
                    stat = item.stat()
                    size_kb = stat.st_size / 1024
                    mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    files_data.append({
                        "filename": item.name,
                        "size": f"{size_kb:.1f} KB",
                        "date": mod_time
                    })
        except Exception as e:
            print(f"Error reading quarantine: {e}")
            return "[]"
            
        return json.dumps(files_data)
        
    @Slot()
    def clear_threat_logs(self):
        log_path = Path(self._project_root) / "threat_log.txt"
        try:
            if log_path.exists():
                log_path.unlink()
            self._threats_blocked = "0"
            self.threatsBlockedChanged.emit()
            self._save_session()
            self.set_backend_status("Threat logs cleared.")
        except Exception as e:
            self.set_backend_status(f"Error clearing logs: {e}")
