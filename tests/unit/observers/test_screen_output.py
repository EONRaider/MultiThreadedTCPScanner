from src.core.types import PortState, ScanResult
from src.modules.output.screen import ScreenOutput
from src.modules.scan_modes.tcp_connect import TCPConnect


class TestScreenOutput:
    def test_screen_init(self, mock_tcp_connect):
        screen_observer = ScreenOutput(mock_tcp_connect)
        assert isinstance(screen_observer.scanner, TCPConnect)

    def test_screen_startup(self, mocker, capsys, mock_tcp_connect):
        # Mock the call to time.ctime so all tests make use of the same
        # value for the current time despite the environment
        time_now = "Sun Jan 1 00:00:00 2023"
        mocker.patch("src.modules.output.screen.ctime", return_value=time_now)

        screen_observer = ScreenOutput(mock_tcp_connect)
        screen_observer.startup()

        # Capture all output from calls to print
        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] Starting port scanner at {time_now}\n"
            f"[+] Scan results for {mock_tcp_connect.target}\n"
        )

    def test_screen_cleanup(self, capsys, mock_tcp_connect):
        total_time = 2.0
        mock_tcp_connect.total_time = total_time
        screen_observer = ScreenOutput(mock_tcp_connect)
        screen_observer.cleanup()

        # Capture all output from calls to print
        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] TCP-connect scan of {mock_tcp_connect.num_ports} ports for "
            f"{mock_tcp_connect.target} completed in {total_time:.2f} seconds\n"
        )

    def test_screen_update(self, capsys, mock_tcp_connect):
        ScreenOutput(mock_tcp_connect)
        for port in mock_tcp_connect.ports:
            result = ScanResult(port, PortState.OPEN)
            mock_tcp_connect._notify_all(result)

            # Capture all output from calls to print
            captured = capsys.readouterr()

            assert captured.out == f"\t{result}\n"
