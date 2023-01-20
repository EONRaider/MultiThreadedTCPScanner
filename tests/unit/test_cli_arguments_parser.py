import pytest

from src.modules.cli import CLIArgumentsParser


class TestCLIArgumentsParser:
    def test_parse_port_ranges(self):
        parser = CLIArgumentsParser()
        args = parser.parse(["target.com", "--ports", "20-25, 80,111, 443"])
        assert args.target == "target.com"
        assert args.ports == (20, 21, 22, 23, 24, 25, 80, 111, 443)
        assert args.timeout == 1.0

    def test_parse_all_ports(self):
        parser = CLIArgumentsParser()
        args = parser.parse(["target.com", "--all"])
        assert args.ports == tuple(range(1, 65536))

    @pytest.mark.parametrize("invalid_input", ["20=25, abc*def, a+b"])
    def test_invalid_syntax(self, invalid_input):
        parser = CLIArgumentsParser()
        with pytest.raises(SystemExit):
            parser.parse(["target.com", "--ports", invalid_input])
