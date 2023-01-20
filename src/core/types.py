from dataclasses import dataclass
from enum import Enum


class PortState(Enum):
    UNDEFINED = "Undefined"
    OPEN = "Open | SYN / ACK"
    TIMEOUT = "Closed | No Response"
    CONNREFUSED = "Closed | Connection Refused"
    NETERROR = "Network Error"


@dataclass
class ScanResult:
    port: int
    state: PortState = PortState.UNDEFINED
