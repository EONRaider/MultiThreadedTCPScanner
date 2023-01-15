#!/bin/python3

import socket
import sys

def print_help_message():
    print("""
    Usage: ./port-scanner [HOSTNAME] [PORT]

    [PORT]: specify a single port, multiple ports separated by commas or 'a' for all ports
    """)
    sys.exit()

def handle_arguments():
    if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        print_help_message()
    elif len(sys.argv) != 3:
        print_help_message()
    else:
        scan_ports()

def scan_all_ports():
    HOST = sys.argv[1]
    found_open_ports = False
    for i in range(1, 65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((HOST, i))
        if result == 0:
            print(f"Port {i} on {HOST} is open.")
            found_open_ports = True
    if not found_open_ports:
        print(f"Could not detect any open ports on {HOST}")
    sock.close()

def scan_multiple_ports():
    HOST = sys.argv[1]
    PORTS = sys.argv[2]
    ports_list = PORTS.split(",")
    found_open_ports = False
    for p in ports_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((HOST, int(p)))
        if result == 0:
            print(f"Port {p} on {HOST} is open.")
            found_open_ports = True
    if not found_open_ports:
        print(f"None of the specified ports are open on {HOST}")
    sock.close()

def scan_single_port():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((HOST, PORT))
    if result == 0:
        print(f"Port {PORT} on {HOST} is open.")
    else:
        print(f"Port {PORT} on {HOST} is closed.")
    sock.close()


def scan_ports():
    if sys.argv[2] == "-a":
        scan_all_ports()
    else:
        PORTS = sys.argv[2]
        if "," in PORTS:
            scan_multiple_ports()
        else:
            scan_single_port()

if __name__ == "__main__":
    handle_arguments()
