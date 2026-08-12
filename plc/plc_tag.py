from dataclasses import dataclass


@dataclass(slots=True)
class PLCTag:
    """
    Represents a single monitored value inside the PLC.

    Each row in the Monitor sheet will become one PLCTag object.

    Example:
        Room 101 Temperature
        DB1
        REAL
        Offset 0.0
    """

    ahu: str
    room_no: str
    room_name: str

    parameter: str

    db: int
    datatype: str
    offset: float