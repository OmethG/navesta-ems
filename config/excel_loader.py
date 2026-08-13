from pathlib import Path

import pandas as pd

from plc.plc_tag import PLCTag

from plc.alarm_tag import AlarmTag


class ExcelLoader:
    """
    Loads configuration data from Details.xlsx.
    """

    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)

        if not self.excel_path.exists():
            raise FileNotFoundError(
                f"Excel file not found:\n{self.excel_path}"
            )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _validate_columns(
        self,
        dataframe,
        required_columns,
        sheet_name
    ):
        """
        Validate that all required columns exist.
        """

        missing = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing:
            raise ValueError(
                f"{sheet_name} sheet is missing required column(s): "
                f"{', '.join(missing)}"
            )

    # ---------------------------------------------------------
    # Dashboard Layout
    # ---------------------------------------------------------

    def load_dashboard(self):
        """
        Loads AHUs and Rooms from the Name sheet.
        """

        df = pd.read_excel(
            self.excel_path,
            sheet_name="Name"
        )

        df = df.fillna("")

        df = df[
            ~(df.astype(str)
              .apply(lambda x: x.str.strip())
              .eq("")
              .all(axis=1))
        ]

        columns = list(df.columns)

        if len(columns) < 3:
            raise ValueError(
                "The 'Name' sheet must contain at least 3 columns."
            )

        ahu_col = columns[0]
        room_col = columns[1]
        room_no_col = columns[2]

        ahus = []

        current = None

        for _, row in df.iterrows():

            ahu = str(row[ahu_col]).strip()
            room = str(row[room_col]).strip()
            room_no = str(row[room_no_col]).strip()

            if ahu != "":

                current = {
                    "ahu": ahu,
                    "rooms": []
                }

                ahus.append(current)

            if current is None:
                continue

            if room == "":
                continue

            current["rooms"].append(
                {
                    "room_name": room,
                    "room_no": room_no,

                    # Placeholder values
                    "temperature": 22.5,
                    "humidity": 48,
                    "pressure": 15,

                    "temperature_state": "normal",
                    "humidity_state": "normal",
                    "pressure_state": "normal",
                }
            )

        return ahus

    # ---------------------------------------------------------
    # PLC Monitor Tags
    # ---------------------------------------------------------

    def load_monitor_tags(self):
        """
        Loads PLC monitoring tags from the Monitor sheet.
        """

        df = pd.read_excel(
            self.excel_path,
            sheet_name="Monitor"
        )

        df = df.fillna("")

        required_columns = [
            "Name",
            "Room No",
            "Data",
            "DB",
            "Data type",
            "Offset",
        ]

        self._validate_columns(
            dataframe=df,
            required_columns=required_columns,
            sheet_name="Monitor"
        )

        tags = []

        for _, row in df.iterrows():

            name = str(row["Name"]).strip()
            room_no = str(row["Room No"]).strip()
            parameter = str(row["Data"]).strip()

            db = str(row["DB"]).strip()
            datatype = str(row["Data type"]).strip().upper()
            offset = float(row["Offset"])

            # Convert DB1 -> 1
            db = int(db.replace("DB", ""))

            tags.append(
                PLCTag(
                    name=name,
                    room_no=room_no,
                    parameter=parameter,
                    db=db,
                    datatype=datatype,
                    offset=offset,
                )
            )

        return tags

    # ---------------------------------------------------------

    def load_alarm_tags(self):
        """
        Loads PLC alarm bits from the Alarms sheet.
        """

        import re

        df = pd.read_excel(
            self.excel_path,
            sheet_name="Alarms"
        )

        df = df.fillna("")

        required_columns = [
            "Name",
            "DataType",
            "Address",
        ]

        self._validate_columns(
            dataframe=df,
            required_columns=required_columns,
            sheet_name="Alarms"
        )

        #
        # Build room lookup from monitor tags
        #

        monitor_tags = self.load_monitor_tags()


        alarms = []

        for _, row in df.iterrows():

            if str(row["DataType"]).upper() != "BOOL":
                continue

            alarm_name = str(row["Name"]).strip()

            #
            # Determine warning / critical
            # Parse address
            #

            plc_tag = str(row["PLC tag"]).upper()

# -----------------------------
# Alarm Type
# -----------------------------

            if "CRITICAL" in plc_tag:
                alarm_type = "critical"
            else:
                alarm_type = "warning"

            # -----------------------------
            # Parameter
            # -----------------------------

            if "TEMP" in plc_tag:
                parameter = "temperature"

            elif "RH" in plc_tag:
                parameter = "humidity"

            elif "PRESS" in plc_tag:
                parameter = "pressure"

            else:
                continue

            # -----------------------------
            # Room Name
            # -----------------------------

            parts = plc_tag.split(".")

            if len(parts) < 2:
                continue

            room_name = (
                parts[1]
                .replace('"', "")
                .replace("_", "")
                .replace(" ", "")
                .lower()
            )
            
            # -----------------------------
            # Match monitor tag
            # -----------------------------

            matched = None

            alarm_key = (
                room_name
                .replace("_", "")
                .replace(" ", "")
                .replace("-", "")
                .replace("/", "")
                .replace('"', "")
                .lower()
            )

            for tag in monitor_tags:

                monitor_key = (
                    tag.name
                    .replace("_", "")
                    .replace(" ", "")
                    .replace("-", "")
                    .replace("/", "")
                    .replace('"', "")
                    .lower()
                )

                if (
                    alarm_key in monitor_key
                    or monitor_key in alarm_key
                ) and tag.parameter.lower() == parameter:

                    matched = tag
                    break

            if matched is None:
                continue

            print(
                f"{alarm_key} -> {matched.room_no} ({matched.parameter})"
            )

            room_no = matched.room_no



            # Example:
            # %DB101.DBX2.1
            #

            address = str(row["Address"]).strip()

            match = re.search(
                r"DB(\d+)\.DBX(\d+)\.(\d+)",
                address
            )

            if match is None:
                continue

            db = int(match.group(1))
            byte = int(match.group(2))
            bit = int(match.group(3))

            alarms.append(

                AlarmTag(

                    name=alarm_name,

                    room_name=room_name,

                    room_no=room_no,

                    parameter=parameter,

                    alarm_type=alarm_type,

                    db=db,

                    byte=byte,

                    bit=bit,
                )

            )

        return alarms


# -------------------------------------------------------------
# Testing
# -------------------------------------------------------------

if __name__ == "__main__":

    loader = ExcelLoader("data/Details.xlsx")

    alarms = loader.load_alarm_tags()

    print("=" * 80)
    print(f"Alarm Tags Loaded : {len(alarms)}")
    print("=" * 80)

    for alarm in alarms[:10]:
        print(alarm)



    from collections import Counter

    counter = Counter()

    for alarm in alarms:
        counter[(alarm.parameter, alarm.alarm_type)] += 1

    print(counter)