import pytest

from src.core.types import ScanResult, PortState
from src.modules.output.file import FileOutput
from src.modules.scan_modes.tcp_connect import TCPConnect


@pytest.fixture
def file_path(tmp_path):
    return tmp_path / "test_file.txt"


class TestFileOutput:
    def test_file_init(self, file_path, mock_scanner):
        file_observer = FileOutput(mock_scanner, path=file_path)
        assert isinstance(file_observer.scanner, TCPConnect)

    def test_file_startup(self, file_path, mock_scanner):
        file_observer = FileOutput(mock_scanner, path=file_path)
        with mock_scanner:
            # Calls the startup and cleanup methods of FileOutput
            pass
        assert file_observer.path.read_text() == "port,state\n"

    def test_file_cleanup(self, file_path, capsys, mock_scanner):
        FileOutput(mock_scanner, path=file_path)
        with mock_scanner:
            # Calls the startup and cleanup methods of FileOutput
            pass

        # Capture all output from calls to print
        captured = capsys.readouterr()

        assert captured.out == f"[+] Scan results successfully written to {file_path}\n"

    def test_file_update(self, file_path, mock_scanner):
        FileOutput(mock_scanner, path=file_path)
        with mock_scanner:
            for port in mock_scanner.ports:
                result = ScanResult(port, PortState.OPEN)
                mock_scanner._notify_all(result)
        assert (
            file_path.read_text() == "port,state\n"
            "21,Open | SYN / ACK\n"
            "53,Open | SYN / ACK\n"
            "80,Open | SYN / ACK\n"
            "443,Open | SYN / ACK\n"
        )
