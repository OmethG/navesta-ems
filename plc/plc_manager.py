from config.excel_loader import ExcelLoader
from plc.snap7_client import Snap7Client


class PLCManager:
    """
    High-level PLC manager.

    Responsible for:

    - Loading PLC tags
    - Managing the Snap7 client
    - Reading live PLC values
    """

    def __init__(self, excel_path: str):

        self.loader = ExcelLoader(excel_path)

        self.tags = self.loader.load_monitor_tags()

        self.client = Snap7Client()

    # ---------------------------------------------------------

    def connect(self):

        self.client.connect()

    # ---------------------------------------------------------

    def disconnect(self):

        self.client.disconnect()

    # ---------------------------------------------------------

    def get_tags(self):

        return self.tags

    # ---------------------------------------------------------

    def read_all_values(self):
        """
        Reads every PLC tag and returns
        a dictionary of live values.
        """

        values = {}

        for tag in self.tags:

            if tag.datatype == "REAL":

                value = self.client.read_real(
                    tag.db,
                    tag.offset,
                )

                values[(tag.room_no, tag.parameter)] = value

        return values


# -------------------------------------------------------------
# Test
# -------------------------------------------------------------

if __name__ == "__main__":

    plc = PLCManager("data/Details.xlsx")

    plc.connect()

    values = plc.read_all_values()

    print("=" * 80)
    print(f"Values Read : {len(values)}")
    print("=" * 80)

    for key, value in list(values.items())[:20]:
        print(key, "=", value)

    plc.disconnect()