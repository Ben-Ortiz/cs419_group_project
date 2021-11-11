import socket
import select
import errno
import json


HEADER_SIZE = 10



class Client:

	def __init__(self, username, ip, port) -> None:
		self.USERNAME = username
		self.IP = ip
		self.PORT = port

	def connect_to_server(self, reconnect=False):

		"""
		Attempts to connect to server
		
		If no connection, query user if the want to attempt to reconnect
		"""

		#NOTE I haven't really looked at the reconnect stuff yet

		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client_socket.connect((self.IP, self.PORT))
			self.client_socket.setblocking(False)
			print("Client connected to the server")		

			return True

		except ConnectionRefusedError:
			clear()
			print("Client could not connect to server...")
			if not reconnect:
				print("Connection Aborted")
				exit(0)

			return False


	def verify_login(self, password):

		"""
		Verifies login
		"""
		
		packaged_message = {"type":"login_check", "src":self.USERNAME, "dest":"server", "data":password, "is_encrypted":False}
		packet = json.dumps(packaged_message).encode("utf-8")


		username_header = f"{len(packet):<{HEADER_SIZE}}".encode("utf-8") # packet header
		self.client_socket.send(username_header + packet)


	def send_msg(self, message, target):
		
		while True:
			packaged_message = {"type":"message", "src":self.USERNAME, "dest":target, "data":message}
			packet = json.dumps(packaged_message).encode("utf-8")

			packet_header = f"{len(packet):<{HEADER_SIZE}}".encode("utf-8")
			self.client_socket.send(packet_header + packet)


	def recieve_msg(self):

		"""
		Recieves incoming messages
		"""

		try:
            while True:
                # Recieve things
                username_header = self.client_socket.recv(HEADER_SIZE)
                if not len(username_header):
                    print("connection closed by the server")
                    exit()

                # parse header
                username_len = int(username_header.decode("utf-8").strip())
                username = self.client_socket.recv(username_len).decode("utf-8")

                # If message type == ping

                message_header = self.client_socket.recv(HEADER_SIZE)
                message_len = int(message_header.decode("utf-8").strip())
                message = self.client_socket.recv(message_len).decode("utf-8")

                print(f"{username} > {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading Error:", e)
                exit()
            continue

        except Exception as e:
            print("General Error:", e)
            exit()

	
	def query_server(self):
		read, write, err = select.select(self.sockets_list, [], [])

		for s in read: 
			if s == self.c: 
				message = s.recv(2048) 
				print(message)
			else: 
				message = sys.stdin.readline() 
				self.c.send(message) 
				sys.stdout.write("<You>") 
				sys.stdout.write(message) 
				sys.stdout.flush()
