import socket
import sys

if len(sys.argv) != 3:
    print("Usage: ./port-scanner [HOSTNAME] [PORT]")
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex((HOST, PORT))

if result == 0:
    print(f"Port {PORT} on {HOST} is open.")
else:
    print(f"Port {PORT} on {HOST} is closed.")

sock.close()
