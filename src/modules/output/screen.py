from time import ctime, time

from src.modules.core import ScanResult
from src.modules.output.base_processor import OutputProcessor


class ScreenOutput(OutputProcessor):
    def __init__(self, scanner):
        super().__init__(scanner)

    def initialize(self) -> None:
        print(f"[+] Starting port scanner at {ctime(time())}")
        print(f"[+] Scan results for {self.scanner.target}")

    def cleanup(self) -> None:
        print(
            f"[+] TCP-connect scan of {self.scanner.num_ports} ports for "
            f"{self.scanner.target} completed in {self.scanner.total_time:.2f} "
            f"seconds"
        )

    @staticmethod
    def update(result: ScanResult) -> None:
        print(f"\tPort {result.port} is {result.state.value}")
