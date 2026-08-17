import snap7
from snap7.util import get_real, get_bool

from config.plc_config import (
    PLC_IP,
    PLC_RACK,
    PLC_SLOT,
)


class Snap7Client:
    """
    Low-level Siemens PLC client.

    Responsible only for communicating with
    the PLC using the Snap7 library.
    """

    def __init__(self):
        self.client = snap7.client.Client()

    # ---------------------------------------------------------

    def connect(self):
        """
        Connect to the PLC.
        """

        self.client.connect(
            PLC_IP,
            PLC_RACK,
            PLC_SLOT,
        )

    # ---------------------------------------------------------

    def disconnect(self):
        """
        Disconnect from the PLC.
        """

        if self.client.get_connected():
            self.client.disconnect()

    # ---------------------------------------------------------

    def is_connected(self):
        """
        Returns True if connected.
        """

        return self.client.get_connected()

    # ---------------------------------------------------------

    def read_real(
        self,
        db_number: int,
        offset: float,
    ):
        """
        Reads a REAL value.
        """

        data = self.client.db_read(
            db_number,
            int(offset),
            4,
        )

        return get_real(data, 0)

    # ---------------------------------------------------------

    def read_db(
        self,
        db_number: int,
        start: int,
        size: int,
    ):
        """
        Reads an entire block from a PLC DB.
        """

        return self.client.db_read(
            db_number,
            start,
            size,
        )

    # ---------------------------------------------------------

    def read_bool(
        self,
        db_number: int,
        byte_offset: int,
        bit_offset: int,
    ):
        """
        Reads a BOOL value.

        Example:
            %DB101.DBX2.1

            db_number = 101
            byte_offset = 2
            bit_offset = 1
        """

        data = self.client.db_read(
            db_number,
            byte_offset,
            1,
        )

        return get_bool(
            data,
            0,
            bit_offset,
        )


# -------------------------------------------------------------
# Test
# -------------------------------------------------------------

if __name__ == "__main__":

    plc = Snap7Client()

    print("=" * 60)
    print("Connecting to PLC...")
    print("=" * 60)

    try:

        plc.connect()

        print("Connected :", plc.is_connected())

        data = plc.read_db(
            db_number=1,
            start=0,
            size=16,
        )

        print("Raw DB1 Bytes:", data)

        value = plc.read_real(
            db_number=1,
            offset=0,
        )

        print(f"DB1.DBD0 = {value}")

        # Example BOOL read
        alarm = plc.read_bool(
            db_number=101,
            byte_offset=2,
            bit_offset=0,
        )

        print(f"DB101.DBX2.0 = {alarm}")

    except Exception as e:

        print("\nConnection / Read Failed")
        print(e)

    finally:

        plc.disconnect()

        print("Disconnected.")