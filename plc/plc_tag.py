from dataclasses import dataclass


@dataclass(slots=True)
class PLCTag:
    """
    Represents a single PLC monitoring tag from the
    Monitor sheet in Read_Data.xlsx.
    """

    # Display name from the Monitor sheet
    name: str

    # Room number (e.g. G024)
    room_no: str

    # Temperature / RH / Pressure
    parameter: str

    # PLC information
    db: int
    datatype: str
    offset: float