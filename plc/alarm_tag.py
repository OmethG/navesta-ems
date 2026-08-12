from dataclasses import dataclass


@dataclass
class AlarmTag:
    """
    Represents one PLC alarm bit.

    Example:

        Alarm_Temp_Corridor_Output

    or

        Alarm_Temp_Corridor_Output_Critical
    """

    # PLC tag name
    name: str

    # Room information
    room_name: str
    room_no: str

    # temperature / humidity / pressure
    parameter: str

    # warning / critical
    alarm_type: str

    # PLC address
    db: int
    byte: int
    bit: int