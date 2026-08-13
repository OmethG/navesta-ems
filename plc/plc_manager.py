from config.excel_loader import ExcelLoader
from plc.snap7_client import Snap7Client


class PLCManager:
    """
    High-level PLC Manager.

    Responsible for:

    - Loading PLC tags
    - Managing the Snap7 client
    - Reading live PLC values
    - Returning values grouped by room
    """

    def __init__(self, excel_path: str):

        self.loader = ExcelLoader(excel_path)

        self.tags = self.loader.load_monitor_tags()

        self.alarm_tags = self.loader.load_alarm_tags()

        self.client = Snap7Client()

    # ---------------------------------------------------------

    def connect(self):
        """Connect to the PLC."""
        self.client.connect()

    # ---------------------------------------------------------

    def disconnect(self):
        """Disconnect from the PLC."""
        self.client.disconnect()

    # ---------------------------------------------------------

    def get_tags(self):
        """Returns all PLC tags."""
        return self.tags

    # ---------------------------------------------------------

    def read_all_values(self):
        """
        Reads every configured PLC tag.

        Returns
        -------
        dict

        Example:

        {
            "G024": {
                "temperature": 21.0,
                "humidity": 48.2,
                "pressure": 15.0,
            },

            "G027": {
                "temperature": 22.4,
                "humidity": 49.1,
                "pressure": 14.8,
            }
        }
        """

        values = {}

        for tag in self.tags:

            if tag.datatype != "REAL":
                continue

            value = self.client.read_real(
                tag.db,
                tag.offset,
            )

            room = tag.room_no

            parameter = tag.parameter.lower()

            # Normalize PLC parameter names
            if parameter == "rh":
                parameter = "humidity"

            if room not in values:
                values[room] = {}

            values[room][parameter] = value

        return values

    # ---------------------------------------------------------

    def read_alarm_bits(self):
        """
        Reads all PLC alarm bits.
        """

        alarms = {}

        for tag in self.alarm_tags:

            value = self.client.read_bool(
                db_number=tag.db,
                byte_offset=tag.byte,
                bit_offset=tag.bit,
            )

            key = (
                tag.room_no,
                tag.parameter,
                tag.alarm_type,
            )

            alarms[key] = value

        return alarms

        # ---------------------------------------------------------

    def read_dashboard_data(self):
        """
        Returns all live dashboard data including
        values and alarm states.
        """

        values = self.read_all_values()
        alarm_bits = self.read_alarm_bits()

        for room_no, room in values.items():

            # Default states
            room["temperature_state"] = "normal"
            room["humidity_state"] = "normal"
            room["pressure_state"] = "normal"

            # Temperature alarms
            if alarm_bits.get((room_no, "temperature", "critical"), False):
                room["temperature_state"] = "alarm"

            elif alarm_bits.get((room_no, "temperature", "warning"), False):
                room["temperature_state"] = "warning"

        return values

# -------------------------------------------------------------
# Test
# -------------------------------------------------------------

if __name__ == "__main__":

    plc = PLCManager("data/Details.xlsx")

    plc.connect()

    values = plc.read_all_values()

    alarm_bits = plc.read_alarm_bits()

    print("=" * 80)
    print(f"Rooms Read : {len(values)}")
    print("=" * 80)

    for room_no, room_values in list(values.items())[:5]:

        print(room_no)

        for parameter, value in room_values.items():

            print(f"   {parameter:<12} = {value}")

        print()

    print("=" * 80)
    print("Alarm Bits")
    print("=" * 80)

    for key, value in list(alarm_bits.items())[:20]:
        print(key, "=", value)

    plc.disconnect()