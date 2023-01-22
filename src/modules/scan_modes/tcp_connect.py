import socket
from collections.abc import Collection, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, suppress
from time import perf_counter

from src.core.types import ScanResult, PortState
from src.modules.output.base_processor import OutputProcessor


class TCPConnect:
    def __init__(
        self, *, target: str, ports: Collection[int], timeout: float, max_threads: int
    ):
        """
        Mode of operation for the execution of a port scan of the
        TCP-connect type.

        :param target: Hostname of the target to be scanned.
        :param ports: A comma-separated list of ports and/or port ranges
            to scan.
        :param timeout: Time in seconds to wait for a host's response
            before giving up and considering the port as closed.
        """
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.max_threads = max_threads
        self.results: list[ScanResult] = []
        self._observers: list[OutputProcessor] = []
        self.start_time = float()
        self.total_time = float()

    def __enter__(self) -> None:
        """
        Call the startup method of each observer upon execution of an
        instance of TCPConnect as a context manager.
        """
        [observer.startup() for observer in self._observers]

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Call the cleanup method of each observer upon termination of an
        instance of TCPConnect as a context manager.
        """
        [observer.cleanup() for observer in self._observers]

    @contextmanager
    def _timer(self) -> None:
        """
        Auxiliary timer meant to be called as a context manager. Tracks
        the total time it takes to perform a complete scan operation.
        """
        self.start_time = perf_counter()
        yield
        self.total_time = perf_counter() - self.start_time

    @property
    def num_ports(self) -> int:
        """
        An integer representing the total number of ports probed by the
        scanner.
        """
        return len(self.ports)

    def register(self, observer: OutputProcessor) -> None:
        """
        Attach an observer to the scanner for further processing and/or
        output of scan results.

        :param observer: An object implementing the interface of
        OutputProcessor.
        """
        self._observers.append(observer)

    def unregister(self, observer: OutputProcessor) -> None:
        """
        Remove an observer previously attached to the scanner.

        :param observer: An object implementing the interface of
        OutputProcessor.
        """
        with suppress(ValueError):
            # Supress exceptions raised by an attempt to unregister a
            # non-existent observer
            self._observers.remove(observer)

    def _notify_all(self, result: ScanResult) -> None:
        """
        Notify all registered observers of a scan result for further
        processing and/or output.
        :param result: An instance of the ScanResult dataclass.
        """
        [observer.update(result) for observer in self._observers]

    def _probe_target_port(self, port: int) -> ScanResult:
        """
        Send a TCP-connect probe to a target port.

        :param port: The port number to send a TCP-connect probe to.
        :return: An object of type ScanResult representing the port
        number and its state.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            try:
                result = ScanResult(port)
                sock.connect((self.target, port))
            except socket.timeout:
                result.state = PortState.TIMEOUT
            except ConnectionRefusedError:
                result.state = PortState.CONNREFUSED
            except OSError as exc:
                result.state = PortState.NETERROR
                raise exc
            else:
                result.state = PortState.OPEN
        return result

    def execute(self) -> Iterator[ScanResult]:
        """
        Run a TCP-connect scan on all ports of a given target host.

        :return: An iterator of objects of type ScanResult, one for each
        scanned port.
        """
        with self._timer():
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                try:
                    for result in executor.map(self._probe_target_port, self.ports):
                        self.results.append(result)
                        self._notify_all(result)
                        yield result
                except OSError as exc:
                    yield exc
