#!/usr/bin/python3
from modules.cli import CLIArgumentsParser
from modules.exceptions import PortScannerException
from modules.output.file import FileOutput
from modules.output.screen import ScreenOutput
from modules.tcp_connect import TCPConnectScanner


class PortScanner:
    def __init__(self):
        self.cli_args = CLIArgumentsParser().parse()
        self.tcp_connect = TCPConnectScanner(
            target=self.cli_args.target,
            ports=self.cli_args.ports,
            timeout=self.cli_args.timeout,
        )

    def execute(self) -> None:
        ScreenOutput(scanner=self.tcp_connect)
        if self.cli_args.output is not None:
            FileOutput(scanner=self.tcp_connect, path=self.cli_args.output)

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
    PortScanner().execute()
