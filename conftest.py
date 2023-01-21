import pytest

from src.modules.scan_modes.tcp_connect import TCPConnect


@pytest.fixture
def mock_tcp_connect():
    return TCPConnect(
        target="non_existent_host_9328jdjks7887s.com",
        ports=[21, 53, 80, 443],
        timeout=1,
    )
