from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from theme import Theme
from widgets.header import Header
from widgets.column_widget import ColumnWidget
from widgets.status_bar import StatusBar

from config.excel_loader import ExcelLoader


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.loader = ExcelLoader("data/Details.xlsx")
        self.ahus = self.loader.load_dashboard()

        self.build_ui()

    # =========================================================

    def build_ui(self):

        root = QVBoxLayout(self)

        self.setStyleSheet(f"""
        background:{Theme.WINDOW};
        """)

        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(6)

        # -----------------------------------------------------

        root.addWidget(Header())

        # -----------------------------------------------------

        body = QHBoxLayout()

        body.setSpacing(14)

        root.addLayout(body)

        # -----------------------------------------------------
        # Split AHUs
        # -----------------------------------------------------

        # Column 1
        # AHU-01 → AHU-08
        column1 = self.ahus[:8]

        # Column 2
        # AHU-09 → AHU-15
        column2 = self.ahus[8:14]

        # Column 3
        # AHU-16 → Other
        column3 = self.ahus[14:]

        # -----------------------------------------------------

        self.columnOne = ColumnWidget(column1)

        self.columnTwo = ColumnWidget(column2)

        self.columnThree = ColumnWidget(column3)

        # =====================================================
        # Master room widget registry
        # =====================================================

        self.room_widgets = {}

        self.room_widgets.update(self.columnOne.room_widgets)
        self.room_widgets.update(self.columnTwo.room_widgets)
        self.room_widgets.update(self.columnThree.room_widgets)

        print(f"Total Rooms Registered: {len(self.room_widgets)}")



        # -----------------------------------------------------
        # ADD COLUMNS
        # -----------------------------------------------------

        # Give slightly less width to the third column since
        # it contains fewer AHUs.

        body.addWidget(
            self.columnOne,
            4
        )

        body.addWidget(
            self.columnTwo,
            3
        )
        

        rightWidget = QWidget()

        rightLayout = QVBoxLayout(rightWidget)

        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setSpacing(0)

        rightLayout.addWidget(self.columnThree)

        rightLayout.addStretch()

        rightLayout.addWidget(
            StatusBar(),
            alignment=Qt.AlignRight
        )

        body.addWidget(
            rightWidget,
            4
)
            

        # -----------------------------------------------------
        # STYLING
        # -----------------------------------------------------

        body.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # -----------------------------------------------------
        # Make columns expand evenly with the window
        # -----------------------------------------------------

        self.columnOne.setMinimumWidth(0)
        self.columnTwo.setMinimumWidth(0)
        self.columnThree.setMinimumWidth(0)

        self.columnOne.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        self.columnTwo.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        self.columnThree.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )



    def update_room_value(
        self,
        room_no: str,
        parameter: str,
        value,
        state: str = "normal"
    ):
        """
        Update a single room value on the dashboard.

        Parameters
        ----------
        room_no : Room number (e.g. G024)

        parameter : temperature | humidity | pressure

        value : New value to display

        state : normal | warning | alarm
        """

        room = self.room_widgets.get(room_no)

        if room is None:
            return

        label = room.get(parameter)

        if label is None:
            return

        # Update value
        label.setText(str(value))

        # Update colour
        label.setStyleSheet(f"""
            color:{Theme.color(state)};
            font-weight:700;
            background:transparent;
        """)