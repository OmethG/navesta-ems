from config.excel_loader import ExcelLoader
from plc.snap7_client import Snap7Client
from snap7.util import get_real, get_bool


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

        # PLC connection state
        self.connected = False

        # ------------------------------------------
        # PLC Block Cache
        # ------------------------------------------

        # Cache for each PLC Data Block
        self.db_cache = {} 

    # ---------------------------------------------------------

    def connect(self):
        """
        Connect to the PLC.

        Returns
        -------
        bool
            True if connected.
        """

        try:

            self.client.connect()

            self.connected = self.client.is_connected()

        except Exception:

            self.connected = False

        return self.connected

    # ---------------------------------------------------------

    def disconnect(self):
        """
        Disconnect from the PLC.
        """

        self.client.disconnect()

        self.connected = False

    def ensure_connected(self):
        """
        Ensures the PLC is connected.
        """

        print("\n==============================")
        print("ensure_connected()")
        print("==============================")
        print("Current connected flag :", self.connected)
        print("Snap7 connected        :", self.client.is_connected())

        # Already connected
        if self.connected and self.client.is_connected():
            print("Already connected.")
            return True

        # Connection lost
        self.connected = False

        try:

            print("Attempting PLC connection...")

            self.client.connect()

            self.connected = self.client.is_connected()

            print("Connected after connect():", self.connected)

        except Exception as e:

            print("Connection Exception:", e)

            self.connected = False

        print("Returning:", self.connected)

        return self.connected

    # ---------------------------------------------------------

    def calculate_db_sizes(self):
        """
        Calculates the number of bytes required
        to read each PLC DB.
        """

        db1_size = 0

        for tag in self.tags:

            end = int(tag.offset) + 4

            if end > db1_size:
                db1_size = end

        db101_size = 0

        for tag in self.alarm_tags:

            end = tag.byte + 1

            if end > db101_size:
                db101_size = end

        return db1_size, db101_size    

    # ---------------------------------------------------------

    # ---------------------------------------------------------

    def refresh_db_cache(self):
        """
        Reads every PLC DB once and stores the
        bytes in memory.
        """

        if not self.connected:
            return

        # Find every DB used in the project
        dbs = set()

        for tag in self.tags:
            dbs.add(tag.db)

        for tag in self.alarm_tags:
            dbs.add(tag.db)

        self.db_cache.clear()

        for db in sorted(dbs):

            max_size = 0

            # REAL values
            for tag in self.tags:

                if tag.db != db:
                    continue

                end = int(tag.offset) + 4

                if end > max_size:
                    max_size = end

            # BOOL values
            for tag in self.alarm_tags:

                if tag.db != db:
                    continue

                end = tag.byte + 1

                if end > max_size:
                    max_size = end

            self.db_cache[db] = self.client.read_db(
                db_number=db,
                start=0,
                size=max_size,
            )

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

        if not self.connected:
            return {}

        values = {}

        for tag in self.tags:

            if tag.datatype != "REAL":
                continue

            cache = self.db_cache[tag.db]

            value = get_real(
                cache,
                int(tag.offset),
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

        if not self.connected:
            return {}
        alarms = {}

        for tag in self.alarm_tags:

            try:

                cache = self.db_cache[tag.db]

                value = get_bool(
                    cache,
                    tag.byte,
                    tag.bit,
                )

            except Exception:
                raise

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
        if not self.connected:
            return {}

        self.refresh_db_cache()

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

            # Humidity alarms
            if alarm_bits.get((room_no, "humidity", "critical"), False):
                room["humidity_state"] = "alarm"

            elif alarm_bits.get((room_no, "humidity", "warning"), False):
                room["humidity_state"] = "warning"  

            # Pressure alarms
            if alarm_bits.get((room_no, "pressure", "critical"), False):
                room["pressure_state"] = "alarm"

            elif alarm_bits.get((room_no, "pressure", "warning"), False):
                room["pressure_state"] = "warning"  

        return values

# -------------------------------------------------------------
# Test
# -------------------------------------------------------------

if __name__ == "__main__":

    plc = PLCManager("data/Read_Data.xlsx")

    connected = plc.connect()

    print("Connected:", plc.ensure_connected())

    db1, db101 = plc.calculate_db_sizes()

    print(f"DB1 Size   : {db1}")
    print(f"DB101 Size : {db101}")
    plc.refresh_db_cache()

    print("\nCached DBs:")

    for db, data in plc.db_cache.items():
        print(f"DB{db} -> {len(data)} bytes")

    values = plc.read_all_values()

    alarm_bits = plc.read_alarm_bits()

    print("\n=== G024 Alarm Bits ===")

    for key, value in alarm_bits.items():
        if key[0] == "G024":
            print(key, "=", value)

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