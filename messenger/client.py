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
		self.sockets_list = [self.server]


	def connect_to_server(self, reconnect=False):

		"""
		Attempts to connect to server
		
		If no connection, query user if the want to attempt to reconnect
		"""

		#NOTE I haven't really looked at the reconnect stuff yet

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

			return False


	def send_msg(self, user, msg):

		"""
		Sends message to spefied user
		
		Pings server to see if user is online. If so, it sends the message directly to them.
		If not, it stores the message in messages.csv
		"""

		#TODO check if user is online

		if(user_is_online()):
			# create json package which includes the sender, the recipient and the message
			j = {
				"sender": self.username,
				"recpt": user,
				"message": msg
			}
			self.c.sendall(j)
		else:
			# Store message in messages.csv
			with open('data/messages.csv', 'a') as msg_file:
			csv_writer = csv.writer(msg_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow([user, self.username, msg])


	def user_is_online(self, user):

		"""
		Checks whether or not a user is online
		"""
		# This might not need to be its own method

		# placeholder return value
		return True

	
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
