import socket
import select
import json
import time
import pandas as pd
from messenger import support



# IP = sys.argv[1]
# PORT = sys.argv[2]
IP = "10.0.0.63"
PORT = 8888
HEADER_SIZE = 10



def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_SIZE)

        if not len(message_header):
            print("Client disconnected")
            return False

        message_length = int(message_header.decode("utf-8").strip())

        data = client_socket.recv(message_length)

        return {"header": message_header, "data": data}

    except:
        return False

def send_to(client_sock, data):
    client_sock.sendall(data)



if __name__ == "__main__":  

    # Server Initialization
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((IP, PORT))
    print("Server started")
    print("Waiting for client request..")
    server_socket.listen()

    sockets_list = [server_socket]
    clients = {}


    while True:
        read, _, err = select.select(sockets_list, [], sockets_list)

        for notified in read:

            # Handle New Connections to the Server
            if notified == server_socket:
                client_socket, client_address = server_socket.accept()
                message = recieve_message(client_socket)
                data = json.loads(message["data"].decode("utf-8"))
                user = data["src"]
                password = data["data"]

                accounts = pd.read_csv("data/accounts.csv", index_col=0)
                user_check = user in accounts.index
                if not user_check:
                    print("Username not valid")
                    failure = {"type":"login_check", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                    packet = support.package_message(failure, HEADER_SIZE)
                    client_socket.send(packet)

                    continue

                valid = accounts.loc[user, "password"]

                if user is False or password != valid:
                    print("user validation failed")
                    failure = {"type":"login_check", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                    packet = support.package_message(failure, HEADER_SIZE)
                    client_socket.send(packet)

                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user

                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user}")
                success = {"type":"login_check", "src":"server", "dest":"user", "data":True, "is_encrypted":False}
                packet = support.package_message(success, HEADER_SIZE)
                client_socket.send(packet)

                continue

            # Handle Messages Sent to the Server
            message = recieve_message(notified)
            if not message:
                continue
            user = clients[notified]
            data = message["data"].decode("utf-8")
            data = json.loads(data)

            if data["type"] == "message":
                # Store message in csv
                messages = pd.read_csv("data/messages.csv", index_col=0)
                # TODO: add message to user table

                # Ping user to see if connection is active
                client = clients[data["dest"]] #this line crashes
                ping = {'type': 'ping', 'src': 'server', 'dest': 'server', 'data': 'sending'}
                packet = support.package_message(ping, HEADER_SIZE)
                client.send(packet)

                # If connection is active, send message to User
                client.send(message)
                continue

            if message is False:
                print(f"Closed connection from {clients[notified]['data'].decode('utf-8')}")
                sockets_list.remove(notified)
                del clients[notified]
                continue
            
            print(f"Recieved Message from {user}: {data}")


        for notified in err:
            sockets_list.remove(notified)
            del clients[notified]