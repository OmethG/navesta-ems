from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from theme import Theme
from widgets.header import Header
from widgets.column_widget import ColumnWidget
from widgets.status_bar import StatusBar

from config.excel_loader import ExcelLoader
from plc.plc_manager import PLCManager


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.loader = ExcelLoader("data/Read_Data.xlsx")
        self.ahus = self.loader.load_dashboard()

        self.plc = PLCManager("data/Read_Data.xlsx")

        self.build_ui()

        # --------------------------------------------
        # First PLC Update
        # --------------------------------------------

        # Connect to PLC once
        self.plc.connect()

        # Initial update
        dashboard_data = self.plc.read_dashboard_data()

        self.update_values(dashboard_data)

        # -------------------------------------------------
        # Refresh PLC every second
        # -------------------------------------------------

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_plc)
        self.timer.start(1000)

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

        # -----------------------------------------------------
        # Collect all room widgets
        # -----------------------------------------------------

        self.room_widgets = {}

        self.room_widgets.update(
            self.columnOne.get_room_widgets()
        )

        self.room_widgets.update(
            self.columnTwo.get_room_widgets()
        )

        self.room_widgets.update(
            self.columnThree.get_room_widgets()
        )

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

    # =========================================================
    # LIVE PLC UPDATE
    # =========================================================

    def update_values(self, values):
        """
        Updates all room values on the dashboard.
        """

        for room_no, room_values in values.items():

            if "temperature" in room_values:

                self.update_room_value(
                    room_no,
                    "temperature",
                    room_values["temperature"],
                    room_values.get(
                        "temperature_state",
                        "normal"
                    ),
                )

            if room_no == "G024":
                print(
                    room_no,
                    room_values["humidity"],
                    room_values["humidity_state"],
                )    

            if "humidity" in room_values:

                self.update_room_value(
                    room_no,
                    "humidity",
                    room_values["humidity"],
                    room_values["humidity_state"],
                )

            if "pressure" in room_values:

                self.update_room_value(
                    room_no,
                    "pressure",
                    room_values["pressure"],
                    room_values["pressure_state"],
                )



    def update_room_value(
        self,
        room_no: str,
        parameter: str,
        value,
        state: str = "normal",
    ):
        """
        Update a single room value.
        """

        room = self.room_widgets.get(room_no)

        if room is None:
            return

        label = room.get(parameter)

        if label is None:
            return

        # -----------------------------
        # Update value
        # -----------------------------

        if isinstance(value, float):
            label.setText(f"{value:.1f}")
        else:
            label.setText(str(value))

        # -----------------------------
        # Update colour
        # -----------------------------

        if state == "alarm":
            colour = "#E53935"       # Red

        elif state == "warning":
            colour = "#F9A825"       # Yellow

        else:
            colour = "#16A34A"       # Green

        label.setStyleSheet(f"""
            color:{colour};
            font-weight:700;
            background:transparent;
        """)

    # =========================================================
    # PLC REFRESH
    # =========================================================

    def refresh_plc(self):
        """
        Reads the latest PLC values and updates
        the dashboard.
        """

        try:

            dashboard_data = self.plc.read_dashboard_data()

            self.update_values(
                dashboard_data
            )

        except Exception as e:

            print("PLC Refresh Error:", e)
    # =========================================================
    # CLEANUP
    # =========================================================

    def closeEvent(self, event):
        """
        Disconnect from the PLC when the application closes.
        """

        try:

            if self.timer.isActive():
                self.timer.stop()

            self.plc.disconnect()

        except Exception:
            pass

        event.accept()