import argparse
from typing import Any, Generator


class CLIArgumentsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Scan any number of ports on a target machine",
        )
        self.parsed_args = None

    def parse(self, *args, **kwargs) -> argparse.Namespace:
        self.parser.add_argument(
            "target",
            type=str,
            help="Target machine to scan"
        )
        self.parser.add_argument(
            "-p", "--ports",
            type=str,
            help="Specify ports (separated by a comma if multiple)"
        )
        self.parsed_args = self.parser.parse_args(*args, **kwargs)
        self._process_port_ranges()
        return self.parsed_args

    def _process_port_ranges(self) -> None:
        """Yield an iterator with integers extracted from a string
        consisting of mixed port numbers and/or ranged intervals.
        Ex: From '20-25,53,80,111' to (20,21,22,23,24,25,53,80,111)
        """
        def _parse_ports() -> Generator[int, Any, None]:
            for port in self.parsed_args.ports.split(','):
                try:
                    port = int(port.strip())
                    if not 0 < port < 65536:
                        raise SystemExit(f'Error: Invalid port number {port}.')
                    yield port
                except ValueError:
                    start, end = (int(port) for port in port.split('-'))
                    yield from range(start, end + 1)
        self.parsed_args.ports = tuple(_parse_ports())
