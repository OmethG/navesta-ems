import snap7

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
        self.client.disconnect()

    # ---------------------------------------------------------

    def is_connected(self):
        """
        Returns True if connected.
        """
        return self.client.get_connected()


# -------------------------------------------------------------
# Test
# -------------------------------------------------------------

if __name__ == "__main__":

    plc = Snap7Client()

    print("Connecting to PLC...")

    try:
        plc.connect()

        print("Connected:", plc.is_connected())

    except Exception as e:
        print("Connection Failed!")
        print(e)

    finally:
        plc.disconnect()
        print("Disconnected.")