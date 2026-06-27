import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtQml import QQmlApplicationEngine

from qml_backend import SecureDriveBackend

PROJECT_ROOT = Path(__file__).resolve().parent
SPLASH_LOGO_PATH = PROJECT_ROOT / "Logo - Secure Drive.png"

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #0a0e17;")  # Dark match
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(str(SPLASH_LOGO_PATH)).scaled(600, 400, Qt.KeepAspectRatio))
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(SPLASH_LOGO_PATH)))
    
    splash = SplashScreen()
    splash.show()

    # Init Backend and Engine
    backend = SecureDriveBackend(PROJECT_ROOT)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", backend)

    qml_file = PROJECT_ROOT / "main.qml"

    def show_main_window():
        splash.close()
        engine.load(str(qml_file))
        if not engine.rootObjects():
            sys.exit(-1)

    QTimer.singleShot(3000, show_main_window)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
