#!/usr/bin/python3
from modules.cli import CLIArgumentsParser
from modules.tcp_connect import TCPConnectScanner


class PortScanner:
    def __init__(self):
        self.cli_args = CLIArgumentsParser().parse()
        self.tcp_connect = TCPConnectScanner(
            target=self.cli_args.target,
            ports=self.cli_args.ports,
            timeout=self.cli_args.timeout)

    def execute(self) -> None:
        try:
            for scan_result in self.tcp_connect.execute():
                print(scan_result)
        except KeyboardInterrupt:
            raise SystemExit("[!] Aborting port scanner...")


if __name__ == "__main__":
    PortScanner().execute()
