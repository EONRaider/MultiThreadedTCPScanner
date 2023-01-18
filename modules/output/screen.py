from modules.core import ScanResult
from modules.output.base import OutputProcessor


class ScreenOutput(OutputProcessor):
    def __init__(self, scanner):
        super().__init__(scanner)
        self._initialize()

    def _initialize(self) -> None:
        print(f"[+] Scan results for {self.scanner.target}")

    @staticmethod
    def update(result: ScanResult) -> None:
        print(f"\tPort {result.port} is {result.state.value}")
