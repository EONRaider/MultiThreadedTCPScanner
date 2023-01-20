import socket
from collections.abc import Collection, Iterator
from contextlib import contextmanager
from time import perf_counter

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
        self.start_time = float()
        self.total_time = float()

    def __enter__(self):
        [observer.initialize() for observer in self._observers]

    def __exit__(self, exc_type, exc_val, exc_tb):
        [observer.cleanup() for observer in self._observers]

    @contextmanager
    def _timer(self) -> None:
        self.start_time = perf_counter()
        yield
        self.total_time = perf_counter() - self.start_time

    @property
    def num_ports(self) -> int:
        return len(self.ports)

    def register(self, observer: OutputProcessor) -> None:
        self._observers.append(observer)

    def unregister(self, observer: OutputProcessor) -> None:
        self._observers.remove(observer)

    def _notify_all(self, result: ScanResult) -> None:
        [observer.update(result) for observer in self._observers]

    def _probe_target_port(self, port: int) -> ScanResult:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            try:
                result = ScanResult(port)
                sock.connect((self.target, port))
            except socket.timeout:
                result.state = PortState.TIMEOUT
            except ConnectionRefusedError:
                result.state = PortState.CONNREFUSED
            except OSError:
                result.state = PortState.NETERROR
            else:
                result.state = PortState.OPEN
        return result

    def execute(self) -> Iterator[ScanResult]:
        with self._timer():
            for port in self.ports:
                try:
                    result = self._probe_target_port(port)
                    self.results.append(result)
                    self._notify_all(result)
                    yield result
                except socket.gaierror:
                    yield HostnameResolutionError(
                        f"Failed to connect or resolve hostname to target "
                        f"address {self.target}"
                    )
