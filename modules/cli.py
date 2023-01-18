import argparse
from collections.abc import Iterator
import pathlib
import re


class CLIArgumentsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Scan any number of ports on a target machine",
        )
        self.group = self.parser.add_mutually_exclusive_group()
        self.parsed_args = None

    def parse(self, *args, **kwargs) -> argparse.Namespace:
        self.parser.add_argument("target", type=str, help="Target machine to scan")
        self.group.add_argument(
            "-p",
            "--ports",
            type=str,
            help="Specify ports (separated by a comma if multiple)",
        )
        self.group.add_argument("--all", action="store_true", help="Scan all ports")
        self.parser.add_argument(
            "--timeout",
            type=float,
            default=1.0,
            help="Time to wait for server response before giving up on the "
            "connection attempt (defaults to 1 second)",
        )
        self.parser.add_argument(
            "-o", "--output", type=str, help="Output results to the specified file path"
        )
        self.parsed_args = self.parser.parse_args(*args, **kwargs)
        self.parsed_args.ports = tuple(self._process_port_ranges())
        return self.parsed_args

    def _process_port_ranges(self) -> Iterator[int]:
        """Yield an iterator with integers extracted from a string
        consisting of mixed port numbers and/or ranged intervals.
        Ex: From '20-25,53,80,111' to (20,21,22,23,24,25,53,80,111)
        """
        if self.parsed_args.all is True:
            yield from range(1, 65536)
        else:
            for port in re.split(r"\s*,\s*", self.parsed_args.ports):
                try:
                    port = int(port)
                    if not 0 < port < 65536:
                        raise SystemExit(f"Error: Invalid port number {port}.")
                    yield port
                except ValueError:  # Failed to cast port into integer
                    try:
                        # Interpret string as a range of ports
                        start, end = (int(port) for port in port.split("-"))
                        yield from range(start, end + 1)
                    except ValueError:  # Generic syntax error
                        raise SystemExit(
                            f"Error: Invalid syntax. Run "
                            f"{pathlib.Path(__file__).name} --help for usage "
                            f"instructions."
                        )
