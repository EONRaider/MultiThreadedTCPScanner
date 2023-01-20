from src.modules.cli_parsing import CLIArgumentsParser
from src.port_scanner import PortScanner

if __name__ == "__main__":
    cli_args = CLIArgumentsParser().parse()
    PortScanner(
        target=cli_args.target,
        ports=cli_args.ports,
        timeout=cli_args.timeout,
        output_file_path=cli_args.output,
    ).execute()
