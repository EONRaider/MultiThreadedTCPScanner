from pathlib import Path

from src.core.types import ScanResult
from src.modules.output.base_processor import OutputProcessor


class FileOutput(OutputProcessor):
    def __init__(self, scanner, path: [str, Path]):
        super().__init__(scanner)
        self.path = Path(path)
        self.file = None

    def startup(self) -> None:
        try:
            self.file = self.path.open("a")
            self.file.write("port,state")
        except OSError as e:
            raise SystemExit(f"{e.__class__.__name__}: {e}")

    def cleanup(self) -> None:
        self.file.close()
        print(f"[+] Scan results successfully written to {self.path}")

    def update(self, result: ScanResult) -> None:
        self.file.write(result.csv_str)
