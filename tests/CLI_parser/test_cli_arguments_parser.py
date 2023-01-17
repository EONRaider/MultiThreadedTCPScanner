from modules.cli import CLIArgumentsParser


class TestCLIArgumentsParser:
    def test_init_parser(self):
        parser = CLIArgumentsParser()
        args = parser.parse(["target.com", "--ports", "20-25, 80,111, 443"])
        assert args.target == "target.com"
        assert args.ports == (20, 21, 22, 23, 24, 25, 80, 111, 443)
