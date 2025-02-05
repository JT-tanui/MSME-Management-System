import sys
from PyQt6.QtWidgets import QApplication
from .main_window import MSMEWindow

def main():
    app = QApplication(sys.argv)
    window = MSMEWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()