from pathlib import Path

import pandas as pd


class ExcelLoader:
    """
    Loads AHU and Room information from Details.xlsx

    Expected sheet:
        Name

    Expected columns:
        AHU
        Room Name
        Room Number

    The loader automatically groups rooms under each AHU.
    """

    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)

        if not self.excel_path.exists():
            raise FileNotFoundError(
                f"Excel file not found:\n{self.excel_path}"
            )

    # ---------------------------------------------------------

    def load(self):

        df = pd.read_excel(
            self.excel_path,
            sheet_name="Name"
        )

        df = df.fillna("")

        # remove empty rows
        df = df[
            ~(df.astype(str).apply(lambda x: x.str.strip()).eq("").all(axis=1))
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

            # New AHU starts
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


# -------------------------------------------------------------

if __name__ == "__main__":

    loader = ExcelLoader("data/Details.xlsx")

    ahus = loader.load()

    print("=" * 60)

    print(f"AHUs Found : {len(ahus)}")

    print("=" * 60)

    total_rooms = 0

    for ahu in ahus:

        count = len(ahu["rooms"])

        total_rooms += count

        print(f"{ahu['ahu']:<15} {count} rooms")

    print("=" * 60)

    print("Total Rooms :", total_rooms)