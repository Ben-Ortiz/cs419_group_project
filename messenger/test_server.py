import socket
import time
import json


HEADER_SIZE = 10


if __name__ == "__main__":
    ip = "192.168.1.7"
    port = 1243

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    while True:
        client, address = server.accept()
        print(f"Connection Established - {address[0]}:{address[1]}")

        d = {1: 2, "key2": 2}
        msg = json.dumps(d)

        l = len(msg)
        offset = len(str(l))
        buffer = HEADER_SIZE - offset
        packet = f"{l}" + " "*buffer + msg

        client.send(bytes(packet, "utf-8"))