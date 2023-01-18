import socket
from collections.abc import Collection, Iterator

from modules.core import ScanResult, PortState
from modules.exceptions import HostnameResolutionError
from modules.output.base_processor import OutputProcessor


class TCPConnectScanner:
    def __init__(self, target: str, ports: Collection[int], timeout: float):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.results: list[ScanResult] = []
        self._observers: list[OutputProcessor] = []

    @property
    def num_ports(self) -> int:
        return len(self.ports)

    def register(self, observer: OutputProcessor) -> None:
        self._observers.append(observer)

    def _notify_all(self, result: ScanResult) -> None:
        [observer.update(result) for observer in self._observers]

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
                self._notify_all(result)
            yield result
