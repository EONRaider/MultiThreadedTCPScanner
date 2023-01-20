from src.modules.core import ScanResult, PortState


class TestScanResult:
    def test_default_values(self):
        result = ScanResult(80)
        assert result.port == 80
        assert result.state == PortState.UNDEFINED
        assert result.state.value == "Undefined"

    def test_state_change(self):
        result = ScanResult(80)
        result.state = PortState.OPEN
        assert result.state.value == "Open | SYN / ACK"
        result.state = PortState.TIMEOUT
        assert result.state.value == "Closed | No Response"
        result.state = PortState.CONNREFUSED
        assert result.state.value == "Closed | Connection Refused"
        result.state = PortState.NETERROR
        assert result.state.value == "Network Error"
