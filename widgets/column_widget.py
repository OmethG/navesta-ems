from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from theme import Theme


class ColumnWidget(QWidget):

    def __init__(self, ahus):
        super().__init__()

        self.ahus = ahus

        # Stores references to every room's value labels
        # Key = Room Number
        self.room_widgets = {}

        self.build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        for ahu in self.ahus:

            section = self.create_ahu_section(ahu)

            root.addWidget(section)

            root.addSpacing(4)

        root.addStretch()

        print(self.room_widgets.keys())

    # ==========================================================
    # TABLE HEADER
    # ==========================================================

    def create_table_header(self):

        frame = QFrame()

        frame.setObjectName("TableHeader")

        frame.setStyleSheet("""
        QFrame{
            background:#EEF2F5;
            border-left:none;
            border-right:none;
            border-bottom:1px solid #D8DEE6;
        }
        """)

        frame.setFixedHeight(Theme.TABLE_HEADER_HEIGHT)

        layout = QHBoxLayout(frame)

        layout.setContentsMargins(8, 1, 8, 1)
        layout.setSpacing(0)

        roomNo = QLabel("Room No")
        roomNo.setObjectName("ColumnHeader")
        roomNo.setFixedWidth(Theme.ROOMNO_WIDTH)

        roomName = QLabel("Room Name")
        roomName.setObjectName("ColumnHeader")
        roomName.setFixedWidth(Theme.ROOMNAME_WIDTH)

        temp = QLabel("Temp")
        temp.setObjectName("ColumnHeader")
        temp.setAlignment(Qt.AlignCenter)
        temp.setFixedWidth(Theme.TEMP_WIDTH)

        rh = QLabel("RH")
        rh.setObjectName("ColumnHeader")
        rh.setAlignment(Qt.AlignCenter)
        rh.setFixedWidth(Theme.RH_WIDTH)

        pressure = QLabel("Pressure")
        pressure.setObjectName("ColumnHeader")
        pressure.setAlignment(Qt.AlignCenter)
        pressure.setFixedWidth(Theme.PRESSURE_WIDTH)

        layout.addWidget(roomNo)
        layout.addWidget(roomName)
        layout.addWidget(temp)
        layout.addWidget(rh)
        layout.addWidget(pressure)

        return frame

        # ==========================================================
    # AHU SECTION
    # ==========================================================

    def create_ahu_section(self, ahu):

        section = QFrame()

        section.setObjectName("AHUCard")

        section.setStyleSheet("""
        QFrame#AHUCard{
            background:white;
            border:1px solid #D4DAE2;
            border-radius:0px;
        }
        """)

        root = QVBoxLayout(section)

        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ------------------------------------------------------
        # AHU TITLE
        # ------------------------------------------------------

        title = QLabel(ahu["ahu"])

        title.setFixedHeight(20)

        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        title.setIndent(12)

        title.setStyleSheet(f"""
        background:{Theme.SECTION_HEADER};
        color:white;
        font-size:10pt;
        font-weight:700;
        border:none;
        border-radius:0px;
        """)

        title.setObjectName("SectionTitle")

        root.addWidget(title)

        root.addWidget(self.create_table_header())

        # ------------------------------------------------------
        # ROOMS
        # ------------------------------------------------------

        for index, room in enumerate(ahu["rooms"]):

            row = QFrame()
            row.setFrameShape(QFrame.NoFrame)

            row.setFixedHeight(20)

            if index % 2 == 0:
                row.setStyleSheet("background:white;")
            else:
                row.setStyleSheet("background:#FAFBFC;")

            layout = QHBoxLayout(row)

            layout.setContentsMargins(8, 1, 8, 1)
            layout.setSpacing(0)

            # ==============================================
            # ROOM NUMBER
            # ==============================================

            roomNo = QLabel(room["room_no"])

            roomNo.setObjectName("RoomNo")

            roomNo.setFixedWidth(
                Theme.ROOMNO_WIDTH
            )

            roomNo.setAlignment(
                Qt.AlignLeft | Qt.AlignVCenter
            )

            roomNo.setStyleSheet("""
            color:#1F2937;
            font-size:9pt;
            font-weight:800;
            background:transparent;
            """)

            # ==============================================
            # ROOM NAME
            # ==============================================

            roomName = QLabel(room["room_name"])

            roomName.setObjectName("RoomName")

            roomName.setFixedWidth(Theme.ROOMNAME_WIDTH)

            roomName.setAlignment(
                Qt.AlignLeft | Qt.AlignVCenter
            )

            roomName.setWordWrap(False)

            roomName.setStyleSheet("""
            color:#1F2937;
            font-size:10pt;
            font-weight:600;
            background:transparent;
        """)

            # ==============================================
            # TEMPERATURE
            # ==============================================

            temp = QLabel(f"{room['temperature']:.1f}")

            temp.setObjectName("Value")

            temp.setFixedWidth(
                Theme.TEMP_WIDTH
            )

            temp.setAlignment(Qt.AlignCenter)

            temp.setStyleSheet(f"""
                color:{Theme.color(room['temperature_state'])};
                font-weight:700;
                background:transparent;
            """)

            # ==============================================
            # HUMIDITY
            # ==============================================

            humidity = QLabel(str(room["humidity"]))

            humidity.setObjectName("Value")

            humidity.setFixedWidth(
                Theme.RH_WIDTH
            )

            humidity.setAlignment(Qt.AlignCenter)

            humidity.setStyleSheet(f"""
                color:{Theme.color(room['humidity_state'])};
                font-weight:700;
                background:transparent;
            """)

            # ==============================================
            # PRESSURE
            # ==============================================

            pressure = QLabel(str(room["pressure"]))

            pressure.setObjectName("Value")

            pressure.setFixedWidth(
                Theme.PRESSURE_WIDTH
            )

            pressure.setAlignment(Qt.AlignCenter)

            pressure.setStyleSheet(f"""
                color:{Theme.color(room['pressure_state'])};
                font-weight:700;
                background:transparent;
            """)

            # ==============================================
            # ADD TO ROW
            # ==============================================

            # Store references to the value labels for this room
            self.room_widgets[room["room_no"]] = {
                "temperature": temp,
                "humidity": humidity,
                "pressure": pressure,
            }

            layout.addWidget(roomNo)
            layout.addWidget(roomName)
            layout.addWidget(temp)
            layout.addWidget(humidity)
            layout.addWidget(pressure)

            root.addWidget(row)

            line = QFrame()

            line.setFixedHeight(1)

            line.setStyleSheet("""
            background:#F2F4F7;
            border:none;
            margin-left:10px;
            margin-right:10px;
            """)

            if index < len(ahu["rooms"]) - 1:
                root.addWidget(line)

        # ------------------------------------------------------
        # SPACE AFTER AHU
        # ------------------------------------------------------


    

        return section

    # ==========================================================
    # PUBLIC METHODS
    # ==========================================================

    def get_room_widgets(self):
        """
        Returns all room widget references
        in this column.
        """

        return self.room_widgets