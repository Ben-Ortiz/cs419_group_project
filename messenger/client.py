#Client Script
# Python program to implement client side of chat room. 
import socket
import select
import sys

from support import clear


class Client:

	def __init__(self, ip, port) -> None:
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = ip
		self.port = port
		self.sockets_list = [sys.stdin, self.server]


	# Attempts to connect to server, if no connection, query user if the want to attempt to reconnect
	def connect(self, reconnect=False):
		try:
			self.server.connect((self.IP, self.port))
			print("Client connected to the server")
			return True

		except ConnectionRefusedError:
			clear()
			print("Client could not connect to server...")
			if not reconnect:
				print("Connection Aborted")
				exit(0)
			print("\nAttempting reconnect...")

			return False

	
	def query_server(self):
		read, write, err = select.select(self.sockets_list, [], [])

		for s in read: 
			if s == self.server: 
				message = s.recv(2048) 
				print(message)
			else: 
				message = sys.stdin.readline() 
				self.server.send(message) 
				sys.stdout.write("<You>") 
				sys.stdout.write(message) 
				sys.stdout.flush()


	def close(self):
		self.server.close() 

