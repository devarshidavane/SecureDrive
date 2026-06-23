import os
import subprocess
import sys
from pathlib import Path

import psutil
from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QFileDialog, QMessageBox, QInputDialog, QLineEdit

from ui_secureDrive import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Secure Drive")

        self.project_root = Path(__file__).resolve().parent
        self.scans_dir = self.project_root / "Scans"
        self.full_scan_script_path = str(self.scans_dir / "full_scan.py")
        self.database_update_script_path = str(self.scans_dir / "database.py")
        self.realtime_process = None
        self.realtime_script_path = str(
            self.scans_dir / "Real_time_scan.py"
        )

        self.full_scan_process = None
        self.database_update_process = None
        self._backend_output_buffers = {}
        self._backend_last_output = {}

        self._init_protection_status_label()
        self._init_backend_status_label()
        self._sync_protection_state_from_running_process()

        self.protection_switch.toggled.connect(self.toggle_realtime_protection)
        self.Real_time_scan_logo.clicked.connect(self.switch_to_Protection_page)
        self.System_scan_logo.clicked.connect(self.start_full_scan)
        self.pushButton_3.clicked.connect(self.start_database_update)
        self.Home.clicked.connect(self.switch_to_Homepage)
        self.Protection.clicked.connect(self.switch_to_Protection_page)
        self.Notification.clicked.connect(self.switch_to_Notification_page)
        self.About.clicked.connect(self.switch_to_About_page)
        self.settings.clicked.connect(self.switch_to_Settings_page)

        self.File_scan_logo.clicked.connect(self.start_file_scan)
        self.Password_breach_logo.clicked.connect(self.check_password_breach)
        self.pushButton_9.clicked.connect(self.check_email_breach)

    def switch_to_Homepage(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_Protection_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_Notification_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_About_page(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_Settings_page(self):
        self.stackedWidget.setCurrentIndex(4)

    def _init_protection_status_label(self):
        self.protection_status_label = QLabel("Protection Status: OFF")
        self.protection_status_label.setObjectName("protection_status_label")
        self.protection_status_label.setStyleSheet(
            "color: #ff5c5c; font-size: 13px; font-weight: 700;"
        )
        self.protection_status_label.setAlignment(Qt.AlignCenter)
        self.gridLayout_10.addWidget(self.protection_status_label, 2, 0, 1, 1)

    def _init_backend_status_label(self):
        self.backend_status_label = QLabel("No scan activity yet.")
        self.backend_status_label.setObjectName("backend_status_label")
        self.backend_status_label.setGeometry(40, 95, 720, 60)
        self.backend_status_label.setWordWrap(True)
        self.backend_status_label.setStyleSheet(
            "color: #ffffff; font-size: 13px; font-weight: 600;"
        )
        self.backend_status_label.setParent(self.Notification_page)
        self.backend_status_label.show()

    def _set_backend_status(self, message: str, success: bool | None = None):
        if success is True:
            color = "#4caf50"
        elif success is False:
            color = "#ff5c5c"
        else:
            color = "#ffffff"

        self.backend_status_label.setText(message)
        self.backend_status_label.setStyleSheet(
            f"color: {color}; font-size: 13px; font-weight: 600;"
        )
        print(f"[SecureDrive] {message}")

    def _set_protection_ui_state(self, enabled: bool):
        self.protection_switch.blockSignals(True)
        self.protection_switch.setChecked(enabled)
        self.protection_switch.blockSignals(False)

        if enabled:
            self.protection_status_label.setText("Protection Status: ON")
            self.protection_status_label.setStyleSheet(
                "color: #4caf50; font-size: 13px; font-weight: 700;"
            )
        else:
            self.protection_status_label.setText("Protection Status: OFF")
            self.protection_status_label.setStyleSheet(
                "color: #ff5c5c; font-size: 13px; font-weight: 700;"
            )

    def _iter_realtime_processes(self):
        target_script = os.path.normcase(os.path.abspath(self.realtime_script_path))
        for proc in psutil.process_iter(["pid", "cmdline"]):
            try:
                cmdline = proc.info.get("cmdline") or []
                normalized_cmdline = [
                    os.path.normcase(os.path.abspath(part))
                    for part in cmdline
                    if isinstance(part, str) and part
                ]
                if target_script in normalized_cmdline:
                    yield proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def _sync_protection_state_from_running_process(self):
        existing = next(self._iter_realtime_processes(), None)
        if existing:
            self.realtime_process = existing
            self._set_protection_ui_state(True)
        else:
            self._set_protection_ui_state(False)

    def toggle_realtime_protection(self, checked):
        if checked:
            self.start_realtime()
        else:
            self.stop_realtime()

    def start_realtime(self):
        try:
            existing = next(self._iter_realtime_processes(), None)
            if existing:
                self.realtime_process = existing
                self._set_protection_ui_state(True)
                print("[SecureDrive] Real-time protection already running.")
                return

            self.realtime_process = subprocess.Popen(
                [sys.executable, self.realtime_script_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                close_fds=True,
            )
            self._set_protection_ui_state(True)
            self._set_backend_status("Real-time protection is running.", True)
        except Exception as e:
            self._set_protection_ui_state(False)
            self._set_backend_status(f"Error starting real-time protection: {e}", False)

    def _terminate_process_tree(self, proc: psutil.Process):
        try:
            children = proc.children(recursive=True)
            for child in children:
                child.terminate()
            _, alive_children = psutil.wait_procs(children, timeout=3)
            for child in alive_children:
                child.kill()

            proc.terminate()
            try:
                proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    def stop_realtime(self):
        try:
            targets = list(self._iter_realtime_processes())
            for proc in targets:
                self._terminate_process_tree(proc)

            self.realtime_process = None
            self._set_protection_ui_state(False)
            self._set_backend_status("Real-time protection stopped.", None)
        except Exception as e:
            self._set_backend_status(f"Error stopping real-time protection: {e}", False)

    def _start_backend_process(self, script_path: str, process_attr: str, label: str):
        existing = getattr(self, process_attr)
        if existing and existing.state() != QProcess.ProcessState.NotRunning:
            self._set_backend_status(f"{label} is already running.", None)
            self.switch_to_Notification_page()
            return

        if not os.path.exists(script_path):
            self._set_backend_status(f"{label} script not found: {script_path}", False)
            self.switch_to_Notification_page()
            return

        try:
            process = QProcess(self)
            process.setProgram(sys.executable)
            process.setArguments(["-u", script_path])
            process.setWorkingDirectory(str(self.project_root))
            process.setProcessChannelMode(
                QProcess.ProcessChannelMode.MergedChannels
            )
            process.readyReadStandardOutput.connect(
                lambda: self._read_backend_output(process, process_attr)
            )
            process.finished.connect(
                lambda exit_code, exit_status: self._finish_backend_process(
                    process,
                    process_attr,
                    label,
                    exit_code,
                    exit_status,
                )
            )

            setattr(self, process_attr, process)
            self._backend_output_buffers[process_attr] = ""
            self._backend_last_output[process_attr] = ""
            process.start()

            if not process.waitForStarted(1500):
                raise RuntimeError(process.errorString())

            self._set_backend_status(f"{label} started.", True)
            self.switch_to_Notification_page()
        except Exception as e:
            setattr(self, process_attr, None)
            self._set_backend_status(f"Error starting {label.lower()}: {e}", False)
            self.switch_to_Notification_page()

    def _read_backend_output(self, process: QProcess, process_attr: str):
        output = bytes(process.readAllStandardOutput()).decode(
            "utf-8",
            errors="replace",
        )
        buffered = self._backend_output_buffers.get(process_attr, "") + output
        lines = buffered.splitlines(keepends=True)

        if lines and not lines[-1].endswith(("\n", "\r")):
            self._backend_output_buffers[process_attr] = lines.pop()
        else:
            self._backend_output_buffers[process_attr] = ""

        for line in lines:
            message = line.strip()
            if not message:
                continue
            self._backend_last_output[process_attr] = message
            self._set_backend_status(message, None)

    def _finish_backend_process(
        self,
        process: QProcess,
        process_attr: str,
        label: str,
        exit_code: int,
        exit_status: QProcess.ExitStatus,
    ):
        self._read_backend_output(process, process_attr)
        trailing_output = self._backend_output_buffers.pop(process_attr, "").strip()
        if trailing_output:
            self._backend_last_output[process_attr] = trailing_output

        last_output = self._backend_last_output.pop(process_attr, "")
        succeeded = (
            exit_status == QProcess.ExitStatus.NormalExit
            and exit_code == 0
        )

        if succeeded:
            message = last_output or f"{label} completed successfully."
            self._set_backend_status(message, True)
        else:
            detail = f" Last output: {last_output}" if last_output else ""
            self._set_backend_status(
                f"{label} failed with exit code {exit_code}.{detail}",
                False,
            )

        if getattr(self, process_attr) is process:
            setattr(self, process_attr, None)
        process.deleteLater()

    def start_full_scan(self):
        self._start_backend_process(
            self.full_scan_script_path,
            "full_scan_process",
            "Full system scan",
        )

    def start_database_update(self):
        self._start_backend_process(
            self.database_update_script_path,
            "database_update_process",
            "Database update",
        )

    def start_file_scan(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Scan")
        if not file_path:
            return
            
        import sys
        if str(self.scans_dir) not in sys.path:
            sys.path.append(str(self.scans_dir))
            
        try:
            from scanner import scan_file
            self._set_backend_status(f"Scanning file: {file_path}", None)
            is_threat = scan_file(file_path, quarantine=True)
            if is_threat:
                QMessageBox.warning(self, "Threat Detected", "The file is a threat and has been quarantined.")
                self._set_backend_status("File scan complete: Threat quarantined.", False)
            else:
                QMessageBox.information(self, "Scan Complete", "No threats found in the file.")
                self._set_backend_status("File scan complete: Clean.", True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to scan file: {e}")
            self._set_backend_status(f"File scan error: {e}", False)

    def check_password_breach(self):
        import hashlib
        import requests
        
        password, ok = QInputDialog.getText(self, "Password Check", "Enter password to check:", QLineEdit.Password)
        if ok and password:
            sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_password[:5]
            suffix = sha1_password[5:]
            try:
                response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
                if response.status_code == 200:
                    hashes = (line.split(':') for line in response.text.splitlines())
                    for h, count in hashes:
                        if h == suffix:
                            QMessageBox.warning(self, "Breach Detected", f"This password has been seen {count} times in data breaches! Please do not use it.")
                            return
                    QMessageBox.information(self, "Safe", "Good news! This password was not found in any known data breaches.")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to connect to API: {response.status_code}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def check_email_breach(self):
        import requests
        email, ok = QInputDialog.getText(self, "Email Check", "Enter email to check:")
        if ok and email:
            # HIBP requires an API key for email checks.
            # Using a placeholder implementation to handle the UI.
            QMessageBox.information(self, "API Key Required", "The Email Breach Check requires a paid HaveIBeenPwned API key. Please implement an alternative API or add your key to the source code.")
