from PySide6.QtGui import QColor


class Theme:

    # ==========================================================
    # WINDOW
    # ==========================================================

    WINDOW = "#F7F9FB"

    HEADER = "#FFFFFF"

    TEXT = "#1F2937"

    SUBTEXT = "#65707C"

    DIVIDER = "#E4E8ED"

    TABLE_HEADER = "#F4F6F8"

    SECTION_HEADER = "#14598A"

    WHITE = "#FFFFFF"

    ALT_ROW = "#F8FAFC"

    # ==========================================================
    # STATUS COLORS
    # ==========================================================

    GREEN = "#2E7D32"

    YELLOW = "#F9A825"

    RED = "#D32F2F"

    # ==========================================================
    # FONTS
    # ==========================================================

    FONT = "Segoe UI"

    TITLE_SIZE = 22

    HEADER_SIZE = 10

    ROOM_SIZE = 11

    VALUE_SIZE = 11

    SMALL_SIZE = 9

    # ==========================================================
    # SIZES
    # ==========================================================

    HEADER_HEIGHT = 72

    TABLE_HEADER_HEIGHT = 22

    ROW_HEIGHT = 18

    COLUMN_SPACING = 8

    SECTION_SPACING = 6

    ROW_SPACING = 0

    # ==========================================================
    # WIDTHS
    # ==========================================================

    ROOMNO_WIDTH = 58

    ROOMNAME_WIDTH = 225

    TEMP_WIDTH = 56

    RH_WIDTH = 50

    PRESSURE_WIDTH = 60

    # ==========================================================

    @staticmethod
    def color(state: str) -> str:
        """
        Returns the display colour for a monitoring state.
        """

        state = state.strip().lower()

        if state == "normal":
            return Theme.GREEN

        if state == "alarm1":
            return Theme.YELLOW

        if state == "alarm2":
            return Theme.RED

        return Theme.TEXT


def stylesheet():

    return f"""
QMainWindow {{
    background: {Theme.WINDOW};
}}

QWidget {{
    font-family: "{Theme.FONT}";
    font-size: {Theme.ROOM_SIZE}pt;
    color: {Theme.TEXT};
}}

QFrame#Header {{
    background: {Theme.HEADER};
    border:none;
    border-bottom:1px solid #C7D0DA;
}}

QLabel#Title {{
    background: transparent;
    color:#111827;
    font-size:22pt;
    font-weight:700;
}}

QLabel#HeaderLabel {{
    background: transparent;
    color: white;
    font-size: 9pt;
}}

QLabel#ColumnHeader {{
    background: transparent;
    color: #425466;
    font-size: {Theme.HEADER_SIZE}pt;
    font-weight: 700;
}}

QLabel#SectionTitle {{
    background: transparent;
    color: white;
    font-size: 10pt;
    font-weight: 700;
}}

QLabel#RoomNo {{
    background:transparent;
    color:#7B8794;
    font-size:9pt;
}}

QLabel#RoomName {{
    background:transparent;
    color:#20262E;
    font-size:10pt;
    font-weight:600;
}}

QLabel#Value {{
    background:transparent;
    font-size:10pt;
    font-weight:700;
}}

QFrame#TableHeader {{
    background: {Theme.TABLE_HEADER};
    border: 1px solid {Theme.DIVIDER};
    border-radius: 4px;
}}

QFrame#Divider {{
    background: {Theme.DIVIDER};
    border: none;
}}
"""