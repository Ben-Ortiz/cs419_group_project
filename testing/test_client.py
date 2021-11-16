import socket
import select
import errno
import json

# size of packets
HEADER_SIZE = 10
IP = "10.0.0.63"
PORT = 8888
USERNAME = input("username? ")
PASSWORD = input("password? ")


if __name__ == "__main__":


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    # verify login
    packaged_message = {"type":"login_check", "src":USERNAME, "dest":"server", "data":PASSWORD, "is_encrypted":False}
    packet = json.dumps(packaged_message).encode("utf-8")


    username_header = f"{len(packet):<{HEADER_SIZE}}".encode("utf-8") # packet header
    client_socket.send(username_header + packet)


    # message sending
    while True:
        # command line input
        # double hitting enter will refresh
        message = input(f"{USERNAME} > ")
        target = input(f"to? > ")

        if message:
            packaged_message = {"type":"message", "src":USERNAME, "dest":target, "data":message}
            print("Test 1")
            print(f"Package: " + packaged_message)
            packet = json.dumps(packaged_message).encode("utf-8")

            packet_header = f"{len(packet):<{HEADER_SIZE}}".encode("utf-8")
            client_socket.send(packet_header + packet)
        
        # Recieving messages
        try:
            while True:
                # Recieve things
                username_header = client_socket.recv(HEADER_SIZE)
                if not len(username_header):
                    print("connection closed by the server")
                    exit()

                # parse header
                username_len = int(username_header.decode("utf-8").strip())
                print("Test 2")
                print(f"Packet header: " + username_len)
                username = client_socket.recv(username_len).decode("utf-8")

                # If message type == ping

                message_header = client_socket.recv(HEADER_SIZE)
                message_len = int(message_header.decode("utf-8").strip())
                message = client_socket.recv(message_len).decode("utf-8")

                print(f"{username} > {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading Error:", e)
                exit()
            continue

        except Exception as e:
            print("General Error:", e)
            exit()
