"""
Heartbeat / liveness check sederhana.

Mencoba membuka koneksi TCP ke host:port. Jika berhasil, server dianggap up.

Pemakaian:
    python check-server.py localhost 44777
"""

import socket
import sys


def check_server(host: str, port: int, timeout: float = 2.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False


def main() -> None:
    if len(sys.argv) != 3:
        print("Pemakaian: python check-server.py <host> <port>")
        raise SystemExit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    if check_server(host, port):
        print("Server up")
    else:
        print("Server down")


if __name__ == "__main__":
    main()
