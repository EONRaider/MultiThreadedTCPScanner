#!/usr/bin/python3
from collections.abc import Collection
from pathlib import Path

from modules.cli import CLIArgumentsParser
from modules.exceptions import PortScannerException
from modules.output.file import FileOutput
from modules.output.screen import ScreenOutput
from modules.tcp_connect import TCPConnectScanner


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
        self.tcp_connect = TCPConnectScanner(
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


if __name__ == "__main__":
    cli_args = CLIArgumentsParser().parse()
    PortScanner(
        target=cli_args.target,
        ports=cli_args.ports,
        timeout=cli_args.timeout,
        output_file_path=cli_args.output,
    ).execute()
