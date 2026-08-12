from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class StatusBar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 12, 8)
        layout.setSpacing(2)

        self.status = QLabel("● PLC Connected")
        self.status.setAlignment(Qt.AlignRight)

        self.status.setStyleSheet("""
            color:#2E7D32;
            font-size:10pt;
            font-weight:700;
        """)

        layout.addWidget(self.status)

        self.updated = QLabel()
        self.updated.setAlignment(Qt.AlignRight)

        self.updated.setStyleSheet("""
            color:#6B7280;
            font-size:9pt;
        """)

        layout.addWidget(self.updated)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        self.updated.setText(
            "Last Updated : " +
            QDateTime.currentDateTime().toString(
                "dd MMM yyyy   hh:mm:ss AP"
            )
        )