#!/usr/bin/python3
from collections.abc import Collection
from pathlib import Path

from src.modules.exceptions import PortScannerException
from src.modules.output.file import FileOutput
from src.modules.output.screen import ScreenOutput
from src.modules.tcp_connect import TCPConnect


class PortScanner:
    def __init__(
        self,
        *,
        target: str,
        ports: Collection[int],
        timeout: float,
        output_file_path: [str, Path] = None,
    ):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.file_path = output_file_path
        self.tcp_connect = TCPConnect(
            target=self.target,
            ports=self.ports,
            timeout=self.timeout,
        )

    def execute(self) -> None:
        ScreenOutput(scanner=self.tcp_connect)
        if self.file_path is not None:
            FileOutput(scanner=self.tcp_connect, path=self.file_path)

        with self.tcp_connect:
            try:
                for result in self.tcp_connect.execute():
                    if isinstance(result, PortScannerException):
                        # Raise exceptions, if any. Else feed the observers
                        # with scan results.
                        raise result
            except KeyboardInterrupt:
                raise SystemExit("[!] TCP port scanner aborted by user. Exiting...")
