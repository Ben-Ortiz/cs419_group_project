import socket
import select
import sys
import support
import encrypt_decrypt_final as ed



HEADER_SIZE = 10



class Client:

	def __init__(self, username, ip, port) -> None:
		self.USERNAME = username
		self.IP = ip
		self.PORT = port
		self.key = None

	def connect_to_server(self, reconnect=False):

		"""
		Attempts to connect to server
		
		If no connection, query user if the want to attempt to reconnect
		"""

		#NOTE I haven't really looked at the reconnect stuff yet

		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client_socket.connect((self.IP, self.PORT))
			# self.client_socket.setblocking(False)
			print("Successfully connected to the server")		

			return True

		except ConnectionRefusedError:
			print("Failure to connect to server...")
			if not reconnect:
				print("Connection Aborted")
				exit(0)

			return False


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


	def verify_login(self, user, password):

		"""
		Returns true if valid login attempt

		Gives client a key
		"""

		dict = {"type":"login_check", "src":user, "dest":"server", "data":password, "is_encrypted":False}

		# send login package to server
		support.send_message(dict, self.client_socket, HEADER_SIZE)

		# wait to hear back from server
		#TODO add some sort of timeout here
		#TODO recieve key from server
		data = support.recieve_message(self.client_socket, HEADER_SIZE)
		dict = support.unpackage_message(data['data'])

		if not dict['data']: return False

		self.key = dict['data']

		return True


	def create_account(self, username, password):

		"""
		Creates new user account and assigns user a key
		"""

		dict = {"type":"account_creation", "src":username, "dest":"server", "data":password, "is_encrypted":False}

		support.send_message(dict, self.client_socket, HEADER_SIZE)

		# wait to hear back from server
		#TODO add some sort of timeout here
		#TODO recieve key from server
		data = support.recieve_message(self.client_socket, HEADER_SIZE)
		dict = support.unpackage_message(data['data'])

		if not dict['data']: return False

		self.key = dict['data']

		return True


	def send_message(self, dest, message):

		"""
		Recieves the destination and the message from app.py
		"""

		m = ed.encrypt(message, self.key, True)
		#print(f"key used to encrypt message: {self.key}")

		dict = {"type":"message", "src":self.USERNAME, "dest":dest, "data":m, "is_encrypted":True}
		support.send_message(dict, self.client_socket, HEADER_SIZE)


	def get_messages(self, user):

		"""
		Retrieves messages with a given user from database and returns array or sm idk yet
		"""

		dict = {"type":"get_convo", "src":self.USERNAME, "dest":"server", "data":user, "is_encrypted":False}

		support.send_message(dict, self.client_socket, HEADER_SIZE)

		return True

	def wait_and_recieve(self):

		"""
		Listens for and recieves any incoming messages, then parses them and performs appropriate actions
		"""

		while True:
			
			# Get new message and convert to python dictionary
			data = support.recieve_message(self.client_socket, HEADER_SIZE)
			if not data:
				print("Disconnected by server")
				break
			dict = support.unpackage_message(data['data'])

			# Parse the dictionary
			type = dict["type"]
			src = dict["src"]
			dest = dict["dest"]

			# Perform appropriate action
			if(type == "message"):
				message = ed.decrypt(dict["data"], self.key, True)
				print(f"New message from {src}: {message}\n")

			if(type == "disconnect"):
				print("This account has been deleted by the admin.")
				break

			if(type == 'conversation_response'):

				m = dict['data']

				print(f'Conversation: \n {m}')