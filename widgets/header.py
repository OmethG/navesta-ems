from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from theme import Theme


class Header(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("Header")
        self.setFixedHeight(Theme.HEADER_HEIGHT)

        self.build_ui()

    # =========================================================

    def build_ui(self):

        layout = QHBoxLayout(self)
        self.setStyleSheet("""
        background:transparent;
        """)

        layout.setContentsMargins(12, 4, 12, 4)
        layout.setSpacing(10)

        # =====================================================
        # LEFT LOGO
        # =====================================================

        self.methgLogo = QLabel()

        self.methgLogo.setStyleSheet("""
        background:transparent;
        border:none;
        """)

        self.methgLogo.setFixedWidth(240)

        self.methgLogo.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )

        pix = QPixmap("assets/methg_logo.png")

        if not pix.isNull():

            self.methgLogo.setPixmap(
                pix.scaled(
                    250,
                    68,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        left = QVBoxLayout()

        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(0)

        left.addStretch()
        left.addWidget(self.methgLogo)
        left.addStretch()

        layout.addLayout(left, 1)

        # =====================================================
        # CENTER
        # =====================================================

        center = QVBoxLayout()

        center.setSpacing(0)

        title = QLabel("Environmental Monitoring System")

        title.setObjectName("Title")

        title.setAlignment(Qt.AlignCenter)

        title.setContentsMargins(0, 2, 0, 0)

        center.addWidget(title)


        layout.addLayout(center, 6)

        # =====================================================
        # RIGHT PANEL
        # =====================================================

        right = QVBoxLayout()

        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)
        right.addStretch()

        self.navestaLogo = QLabel()
        self.navestaLogo.setFixedWidth(240)

        self.navestaLogo.setStyleSheet("""
        background:transparent;
        border:none;
        """)

        self.navestaLogo.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )

        nav = QPixmap("assets/navesta_logo.png")

        if not nav.isNull():

            self.navestaLogo.setPixmap(
                nav.scaled(
                    210,
                    65,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        right.addWidget(self.navestaLogo)

        right.addStretch()

        layout.addLayout(right, 1)

    # =========================================================