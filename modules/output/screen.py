from time import ctime, time

from modules.core import ScanResult
from modules.output.base_processor import OutputProcessor


class ScreenOutput(OutputProcessor):
    def __init__(self, scanner):
        super().__init__(scanner)
        self._initialize()

    def __del__(self):
        print(
            f"[+] TCP-connect scan of {self.scanner.num_ports} ports for "
            f"{self.scanner.target} completed in {self.scanner.total_time:.2f} "
            f"seconds"
        )

    def _initialize(self) -> None:
        print(f"[+] Starting port scanner at {ctime(time())}")
        print(f"[+] Scan results for {self.scanner.target}")

    @staticmethod
    def update(result: ScanResult) -> None:
        print(f"\tPort {result.port} is {result.state.value}")
