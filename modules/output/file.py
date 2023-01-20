from pathlib import Path

from modules.core import ScanResult
from modules.output.base_processor import OutputProcessor


class FileOutput(OutputProcessor):
    def __init__(self, scanner, path: [str, Path]):
        super().__init__(scanner)
        self.path = Path(path)
        self.file = None

    def initialize(self) -> None:
        self.file = self.path.open("a")

    def cleanup(self) -> None:
        self.file.close()
        print(f"[+] Scan results successfully written to {self.path}")

    def update(self, result: ScanResult) -> None:
        self.file.write(f"{result.port}, {result.state.value}\n")
