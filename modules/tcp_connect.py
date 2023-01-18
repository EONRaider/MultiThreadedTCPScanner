import socket
from typing import Collection, Iterator

from modules.core import ScanResult, PortState
from modules.exceptions import HostnameResolutionError
from modules.output.base import OutputProcessor


class TCPConnectScanner:
    def __init__(self, target: str, ports: Collection[int], timeout: int):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.results: list[ScanResult] = []
        self.observers = []

    def register(self, observer: OutputProcessor) -> None:
        self.observers.append(observer)

    def _update_all(self, result: ScanResult) -> None:
        for observer in self.observers:
            observer.update(result)

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
                self._update_all(result)
            yield result
