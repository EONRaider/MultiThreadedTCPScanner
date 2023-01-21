from src.core.types import ScanResult, PortState
from src.port_scanner import PortScanner


class TestPortScanner:
    def test_port_scanner(self, mocker, capsys, file_path):
        target_host = "some-domain.com"
        target_port = 80
        scanner = PortScanner(
            target=target_host,
            ports=[target_port],
            timeout=1.0,
            output_file_path=file_path,
        )

        # Mock the call to TCPConnect._probe_target_port so the creation
        # of a socket FD and a network call are prevented
        mocker.patch(
            "src.modules.scan_modes.tcp_connect.TCPConnect._probe_target_port",
            return_value=(result := ScanResult(target_port, PortState.OPEN)),
        )

        # Mock the call to time.ctime so all tests make use of the same
        # value for the current time despite the environment
        mocker.patch(
            "src.modules.output.screen.ctime",
            return_value=(time_now := "Sun Jan 1 00:00:00 2023"),
        )

        scanner.execute()

        # Capture all output from calls to print
        captured = capsys.readouterr()

        assert captured.out == (
            f"[+] Starting port scanner at {time_now}\n"
            f"[+] Scan results for {target_host}\n"
            f"\tPort {result.port} is {result.state.value}\n"
            f"[+] TCP-connect scan of {scanner.tcp_connect.num_ports} ports for "
            f"{target_host} completed in {scanner.tcp_connect.total_time:.2f} seconds\n"
            f"[+] Scan results successfully written to {file_path}\n"
        )
