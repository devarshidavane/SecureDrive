import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from securedrive import MainWindow

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #FF3131;")  # Set background color to red
        self.label = QLabel(self)
        
        self.label.setPixmap(QPixmap(r"C:\Dmce\Secure drive\UI\QT\Logo - Secure Drive.png").scaled(600, 400, Qt.KeepAspectRatio))
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

def main():
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()

    main_window = MainWindow()

    def show_main_window():
        splash.close()
        main_window.show()

    QTimer.singleShot(3000, show_main_window)  # Show main window after 3 seconds

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
