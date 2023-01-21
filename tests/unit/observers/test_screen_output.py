from src.core.types import PortState, ScanResult
from src.modules.output.screen import ScreenOutput
from src.modules.scan_modes.tcp_connect import TCPConnect


class TestScreenOutput:
    def test_screen_init(self, mock_scanner):
        screen_observer = ScreenOutput(mock_scanner)
        assert isinstance(screen_observer.scanner, TCPConnect)

    def test_screen_startup(self, mocker, capsys, mock_scanner):
        # Mock the call to time.ctime so all tests make use of the same
        # value for the current time despite the environment
        time_now = "Sun Jan 1 00:00:00 2023"
        mocker.patch("src.modules.output.screen.ctime", return_value=time_now)

        screen_observer = ScreenOutput(mock_scanner)
        screen_observer.startup()

        # Capture all output from calls to print
        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] Starting port scanner at {time_now}\n"
            f"[+] Scan results for {mock_scanner.target}\n"
        )

    def test_screen_cleanup(self, capsys, mock_scanner):
        total_time = 2.0
        mock_scanner.total_time = total_time
        screen_observer = ScreenOutput(mock_scanner)
        screen_observer.cleanup()

        # Capture all output from calls to print
        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] TCP-connect scan of {mock_scanner.num_ports} ports for "
            f"{mock_scanner.target} completed in {total_time:.2f} seconds\n"
        )

    def test_screen_update(self, capsys, mock_scanner):
        ScreenOutput(mock_scanner)
        for port in mock_scanner.ports:
            result = ScanResult(port, PortState.OPEN)
            mock_scanner._notify_all(result)

            # Capture all output from calls to print
            captured = capsys.readouterr()

            assert captured.out == f"\t{result}\n"
