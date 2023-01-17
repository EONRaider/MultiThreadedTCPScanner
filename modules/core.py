from dataclasses import dataclass
from enum import Enum


class PortState(Enum):
    UNDEFINED = "Undefined"
    OPEN = "Open"
    TIMEOUT = "Closed | Timeout"
    CONNREFUSED = "Closed | ConnectionRefused"


@dataclass
class ScanResult:
    port: int
    state: PortState = PortState.UNDEFINED
