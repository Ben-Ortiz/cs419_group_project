import socket
import select
import sys
import csv
import json
from messenger.support import clear
from threading import Thread


class Client:

	def __init__(self, username, ip, port) -> None:
		self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.username = username
		self.IP = ip
		self.port = port
		self.sockets_list = [self.c]


	def connect_to_server(self, reconnect=False):

		"""
		Attempts to connect to server
		
		If no connection, query user if the want to attempt to reconnect
		"""

		#NOTE I haven't really looked at the reconnect stuff yet

		try:
			self.c.connect((self.IP, self.port))
			print("Client connected to the server")		

			return True

		except ConnectionRefusedError:
			clear()
			print("Client could not connect to server...")
			if not reconnect:
				print("Connection Aborted")
				exit(0)

			return False


	def send_msg(self, data):

		"""
		Sends message to specified user
		
		Sends message to server, which checks if the recipient is online.
		If so, the server sends the message directly to them.
		If not, the server sends it back, and it is stored in messages.csv (see recieve_msg)

		j: json file containing sender, recipient, and message contents
		"""

		
		self.c.sendall(bytes(data, encoding="utf-8"))


	def recieve_msg(self):

		"""
		Recieves incoming messages

		If the message is addressed to this user, it alerts the user and shows the message.
		If the message is FROM this user, that means the server sent it back (see send_msg) and it should be stored in messages.csv
		"""

		#TODO make it so that it recieves the entire json package before decoding it
		# maybe include length of package in the beginning and/or don't use json (idk I haven't thought about it that much yet)
		while(True):

			j = self.c.recv(2048)
			# Get a json string
			k = json.dumps(j)
			print(k)

			#TODO parse json string and get relevant information (sender, recipient, etc)
			
			#placeholder values
			sender = "Anthony"
			recpt = "Josh"
			msg = "Test message"

			if(sender == self.username):
				# Store message in messages.csv
				with open('data/messages.csv', 'a') as msg_file:
					csv_writer = csv.writer(msg_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
					csv_writer.writerow([user, self.username, msg])

			else:
				#TODO alert user and show message in GUI
				break
			
	
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
