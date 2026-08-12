import snap7
from snap7.util import get_real

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
        Reads a REAL (32-bit floating point) value
        from the specified Data Block.
        """

        data = self.client.db_read(
            db_number,
            int(offset),
            4,
        )

        return get_real(data, 0)


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

        value = plc.read_real(
            db_number=1,
            offset=0,
        )

        print(f"DB1.DBD0 = {value}")

    except Exception as e:

        print("\nConnection / Read Failed")
        print(e)

    finally:

        plc.disconnect()

        print("Disconnected.")