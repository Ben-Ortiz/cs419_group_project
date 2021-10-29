import socket
import json


HEADER_SIZE = 10

if __name__ == "__main__":
    ip = "192.168.1.7"
    port = 1243

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    while True:
        full_msg = ''
        new_msg = True
        while True:
            msg = server.recv(16)

            if new_msg:
                # print(f"new message length: {msg[:HEADER_SIZE]}")
                msglen = int(msg[:HEADER_SIZE])
                new_msg = False

            full_msg += msg.decode("utf-8")

            if len(full_msg) - HEADER_SIZE == msglen:
                # print("full msg recvd")
                d = json.loads(full_msg[HEADER_SIZE:])
                print(d)

                new_msg = True
                full_msg = ''