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

    def __str__(self) -> str:
        return f"Port {self.port} is {self.state.value}"

    @property
    def csv_str(self) -> str:
        """
        Obtain a string representation of the port state in CSV format.
        """
        return f"{self.port},{self.state.value}"
