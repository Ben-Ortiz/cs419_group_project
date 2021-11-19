# from _typeshed import SupportsItemAccess
# from os import SCHED_SPORADIC
import socket
import select
import sys
from messenger import support



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
			# self.client_socket.setblocking(False)
			print("Client connected to the server")		

			return True

		except ConnectionRefusedError:
			print("Client could not connect to server...")
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


	def verify_login(self, login_info):

		"""
		Returns true if valid login attempt
		"""

		# send login package to server
		support.send_message(login_info, self.client_socket, HEADER_SIZE)

		# wait to hear back from server
		#TODO add some sort of timeout here
		data = support.recieve_message(self.client_socket, HEADER_SIZE)
		lib = support.unpackage_message(data['data'])

		return lib["data"]


	def send_message(self, lib):
		
		"""
		Creates json from library, then sends json to the server
		"""

		self.client_socket.sendall(support.package_message(lib, HEADER_SIZE))


	def wait_and_recieve(self):

		"""
		Listens for and recieves any incoming messages, then parses them and performs appropriate actions
		"""

		while True:
			
			# Get new message and convert to python library
			data = support.recieve_message(self.client_socket, HEADER_SIZE)
			if not data:
				print("Disconnected by server")
				exit()
			lib = support.unpackage_message(data['data'])

			# Parse the library
			type = lib["type"]
			src = lib["src"]
			dest = lib["dest"]
			message = lib["data"]

			# Perform appropriate action
			if(type == "message"):
				print(f"user recieved a message from {src}: {message}")