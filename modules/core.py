import socket
from dataclasses import dataclass
from enum import Enum
from typing import Collection, Iterator

from modules.exceptions import HostnameResolutionError


class PortState(Enum):
    UNDEFINED = "Undefined"
    OPEN = "Open"
    TIMEOUT = "Closed | Timeout"
    CONNREFUSED = "Closed | ConnectionRefused"


@dataclass
class ScanResult:
    port: int
    state: PortState = PortState.UNDEFINED


class TCPConnectScanner:
    def __init__(self, target: str, ports: Collection[int], timeout: int):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.results: list[ScanResult] = []

    def execute(self) -> Iterator[ScanResult]:
        for port in self.ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                try:
                    result = ScanResult(port)
                    sock.connect((self.target, port))
                except socket.gaierror:
                    yield HostnameResolutionError(
                        f"Failed to connect or resolve hostname to target "
                        f"address {self.target}"
                    )
                except socket.timeout:
                    result.state = PortState.TIMEOUT
                except ConnectionRefusedError:
                    result.state = PortState.CONNREFUSED
                else:
                    result.state = PortState.OPEN
                self.results.append(result)
            yield result
