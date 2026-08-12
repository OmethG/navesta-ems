import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from dashboard import Dashboard
from theme import stylesheet


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Navesta Environmental Monitoring System")

        # Target design resolution
        self.resize(1920, 1280)

        # Responsive central widget
        self.setCentralWidget(Dashboard())

        # Uncomment for dedicated control-room deployment
        # self.showFullScreen()

        self.setMinimumSize(1400, 900)


def main():

    app = QApplication(sys.argv)

    app.setStyleSheet(stylesheet())

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()