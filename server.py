<<<<<<< Updated upstream
import socket 
import select 
import sys
import json
from threading import Thread



# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit()
=======
import socket
import select
import json
import pandas as pd


HEADER_SIZE = 10
IP = "192.168.1.7"
PORT = 1243


>>>>>>> Stashed changes

def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_SIZE)

        if not len(message_header):
            return False

<<<<<<< Updated upstream

class Server:
    
    def __init__(self, IP, Port):

        """The first argument AF_INET is the address domain of the 
        socket. This is used when we have an Internet Domain with 
        any two hosts The second argument is the type of socket. 
        SOCK_STREAM means that data or characters are read in 
        a continuous flow."""

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.IP = IP
        self.Port = Port

        self.clients = []
        self.threads = []

        """ 
        binds the server to an entered IP address and at the 
        specified port number. 
        The client must be aware of these parameters 
        """
        self.server.bind((IP, Port))
        print("Server started")

        """ 
        listens for active connections. This number can be 
        increased as per convenience. 
        """
        self.server.listen(1)


    def accept_client(self):

        """Accepts a connection request and stores two parameters: 
        client_sock, a socket object for the client that connected, and client_addr, 
        which contains the IP address of that client"""

        print("Waiting for client request..")

        client_sock, client_addr = self.server.accept()

        # List of clients
        self.clients.append(client_sock)

        # prints the address of the user that just connected 
        print(client_addr[0] + " connected")

        # Begin new thread
        t = Thread(target=self.recieve_from, args=(client_sock, client_addr))
        t.start()


    def recieve_from(self, client_sock, client_addr):

        """Recieves outgoing messages from users and sends them to the correct recipient"""

        # loop to recieve messages from client
        while(True):
            data = client_sock.recv(2048)
            j = data.decode("utf-8")
            print(j)

            #placeholder values
            sender = "Anthony"
            recpt = "Josh"
            msg = "Test message"

            # attempt to send message to recipient, if online
            if(False):
                # False is a placeholder for the online status of the recipient
                break
            # return to sender
            else:
                self.send_to(client_sock, data)
=======
        message_length = int(message_header.decode("utf-8").strip())

        return {"header": message_header, "data": client_socket.recv(message_length)}
>>>>>>> Stashed changes

    except:
        return False

    def send_to(self, client_sock, data):
        client_sock.sendall(data)
        

def package_message(data):
    packet = json.dumps(data).encode("utf-8")
    packet_header = f"{len(packet):<{HEADER_SIZE}}".encode("utf-8")
    message = packet_header + packet

<<<<<<< Updated upstream
s = Server(ADDRESS, PORT)

while True:
    try:
        s.server.listen(1)
        s.accept_client()
    except KeyboardInterrupt:
        break
s.server.close()
=======
    return message



if __name__ == "__main__":  

    # Server Initialization
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((IP, PORT))
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
                    packet = package_message(failure)
                    client_socket.send(packet)
                    continue

                valid = accounts.loc[user, "password"]

                if user is False or password != valid:
                    print("user validation failed")
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user

                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user}")
                success = {"type":"login_check", "src":"server", "dest":"user", "data":True, "is_encrypted":False}
                packet = package_message(failure)

            # Handle Messages Sent to the Server
            message = recieve_message(notified)
            user = clients[notified]
            data = message["data"].decode("utf-8")
            data = json.loads(data)

            if data["type"] == "message":
                # Store message in csv
                messages = pd.read_csv("data/messages.csv", index_col=0)
                # TODO: add message to user table

                # Ping user to see if connection is active
                client = clients[data["dest"]]
                ping = {'type': 'ping', 'src': 'server', 'dest': 'server', 'data': 'sending'}
                packet = package_message(ping)
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
>>>>>>> Stashed changes
