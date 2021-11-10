import socket 
import select 
import sys
import json
from threading import Thread



# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit()

# takes the first argument from command prompt as IP address,
# takes second argument from command prompt as port number 
ADDRESS, PORT = str(sys.argv[1]), int(sys.argv[2])



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


    def send_to(self, client_sock, data):
        client_sock.sendall(data)
        


s = Server(ADDRESS, PORT)

while True:
    try:
        s.server.listen(1)
        s.accept_client()
    except KeyboardInterrupt:
        break
s.server.close()