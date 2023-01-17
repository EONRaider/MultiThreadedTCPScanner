#!/usr/bin/python3
import socket

from modules.cli import CLIArgumentsParser


class TCPConnectScanner:
    def __init__(self, target: str, ports: str, all_ports: bool):
        self.target = target
        self.all_ports = all_ports
        self.ports = ports

    def scan_all_ports(self):
        found_open_ports = False
        for i in range(1, 65536):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.target, i))
            if result == 0:
                print(f"Port {i} on {self.target} is open.")
                found_open_ports = True
        if not found_open_ports:
            print(f"Could not detect any open ports on {self.target}")
        sock.close()

    def scan_multiple_ports(self):
        ports_list = self.ports.split(",")
        found_open_ports = False
        for p in ports_list:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.target, int(p)))
            if result == 0:
                print(f"Port {p} on {self.target} is open.")
                found_open_ports = True
        if not found_open_ports:
            print(f"None of the specified ports are open on {self.target}")
        sock.close()

    def scan_single_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.target, int(self.ports)))
        if result == 0:
            print(f"Port {self.ports} on {self.target} is open.")
        else:
            print(f"Port {self.ports} on {self.target} is closed.")
        sock.close()

    def scan_ports(self):
        if self.all_ports:
            self.scan_all_ports()
        else:
            if "," in self.ports:
                self.scan_multiple_ports()
            else:
                self.scan_single_port()


if __name__ == "__main__":
    cli_args = CLIArgumentsParser().parse()

    TCPScanner(
        target=cli_args.target,
        ports=cli_args.ports,
        all_ports=cli_args.all
    ).scan_ports()
