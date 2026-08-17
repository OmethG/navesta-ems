from pathlib import Path

import pandas as pd

from plc.plc_tag import PLCTag

from plc.alarm_tag import AlarmTag

from resource_path import resource_path


class ExcelLoader:
    """
    Loads configuration data from Read_Data.xlsx.
    """

    def __init__(self, excel_path: str):
        self.excel_path = Path(
            resource_path(excel_path)
        )

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
            sheet_name="AHU Rooms"
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
        Loads all alarm bits from the Normal Alarm
        and Critical Alarm sheets.
        """

        alarms = []

        sheets = [
            ("Normal Alarm", "warning"),
            ("Critical Alarm", "critical"),
        ]

        for sheet_name, alarm_type in sheets:

            df = pd.read_excel(
                self.excel_path,
                sheet_name=sheet_name
            )

            df = df.fillna("")

            required_columns = [
                "Room No",
                "Data",
                "DB",
                "Byte_Offset",
                "Bit_Offset",
            ]

            self._validate_columns(
                dataframe=df,
                required_columns=required_columns,
                sheet_name=sheet_name,
            )

            for _, row in df.iterrows():

                parameter = str(row["Data"]).lower()

                if "temp" in parameter:
                    parameter = "temperature"

                elif "rh" in parameter:
                    parameter = "humidity"

                elif "press" in parameter:
                    parameter = "pressure"

                else:
                    continue

                db = int(
                    str(row["DB"]).replace("DB", "")
                )

                alarms.append(

                    AlarmTag(

                        name=str(row["Name"]),

                        room_name=str(row["Name"]),

                        room_no=str(row["Room No"]).strip(),

                        parameter=parameter,

                        alarm_type=alarm_type,

                        db=db,

                        byte=int(row["Byte_Offset"]),

                        bit=int(row["Bit_Offset"]),
                    )

                )

        return alarms


# -------------------------------------------------------------
# Testing
# -------------------------------------------------------------

if __name__ == "__main__":

    loader = ExcelLoader("data/Read_Data.xlsx")

    alarms = loader.load_alarm_tags()

    print("=" * 80)
    print(f"Alarm Tags Loaded : {len(alarms)}")
    print("=" * 80)

    for alarm in alarms:
        if alarm.room_no == "G024":
            print(alarm)



    from collections import Counter

    counter = Counter()

    for alarm in alarms:
        counter[(alarm.parameter, alarm.alarm_type)] += 1

    print(counter)