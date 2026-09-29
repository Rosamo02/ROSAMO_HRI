#Entry point of the application.
#This file initializes the application and starts the graphical interface. It is responsible for setting up the main Qt application environment before displaying the HRI.

import sys
import traceback
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception:
        traceback.print_exc()
        raise
