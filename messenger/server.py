# NOTE: This is just a copy and pasted script, not confirmed to work nor is the functionality complete
# TODO: Review and parse code


#Server Script
import socket 
import select 
import sys
from threading import *


# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 

# takes the first argument from command prompt as IP address,
# takes second argument from command prompt as port number 
ADDRESS, PORT = str(sys.argv[1]), int(sys.argv[2]) 


class Server:
    
    def __init__(self, IP, Port, num_listeners):

        """The first argument AF_INET is the address domain of the 
        socket. This is used when we have an Internet Domain with 
        any two hosts The second argument is the type of socket. 
        SOCK_STREAM means that data or characters are read in 
        a continuous flow."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.IP = IP
        self.Port = Port
        self.listeners = num_listeners

        self.clients = []

        """ 
        binds the server to an entered IP address and at the 
        specified port number. 
        The client must be aware of these parameters 
        """
        self.server.bind((IP, Port))

        """ 
        listens for active connections. This number can be 
        increased as per convenience. 
        """
        self.server.listen(num_listeners)


    def accept(self):
        """Accepts a connection request and stores two parameters, 
        conn which is a socket object for that user, and addr 
        which contains the IP address of the client that just 
        connected"""
        conn, addr = self.server.accept()

        """Maintains a list of clients for ease of broadcasting 
        a message to all available people in the chatroom"""
        self.clients.append(conn)

        # prints the address of the user that just connected 
        print(addr[0] + " connected")


    def clientthread(self, conn, addr): 

        # sends a message to the client whose user object is conn 
        conn.send("Welcome to this chatroom!") 

        while True: 
                try: 
                    message = conn.recv(2048) 
                    if message: 

                        """prints the message and address of the 
                        user who just sent the message on the server 
                        terminal"""
                        print("<" + addr[0] + "> " + message )

                        # Calls broadcast function to send message to all 
                        message_to_send = "<" + addr[0] + "> " + message 
                        self.broadcast(message_to_send, conn) 

                    else: 
                        """message may have no content if the connection 
                        is broken, in this case we remove the connection"""
                        self.remove(conn) 

                except: 
                    continue


    """Using the below function, we broadcast the message to all 
    clients who's object is not the same as the one sending 
    the message """
    def broadcast(self, message, connection): 
        for clients in self.clients: 
            if clients != connection: 
                try: 
                    clients.send(message) 
                except: 
                    clients.close() 

                    # if the link is broken, we remove the client 
                    self.remove(clients) 


    """The following function simply removes the object 
    from the list that was created at the beginning of 
    the program"""
    def remove(self, conn): 
        if conn in self.clients: 
            self.clients.remove(conn) 



server = Server(ADDRESS, PORT, 100)

while True: 

	# creates and individual thread for every user 
	# that connects 
	start_new_thread(server.clientthread,(conn,addr))	 

conn.close() 
server.close()