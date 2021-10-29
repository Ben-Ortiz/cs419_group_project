#Client Script
# Python program to implement client side of chat room. 
import socket
import select
import sys

import json

from messenger.support import clear

from threading import Thread

class thread(Thread):
    def __init__(self, name, ID):
        Thread.__init__(self)
        self.name = name
        self.ID = ID
 
    # helper function to execute the threads
    def run(self):
        print(str(self.name) +" "+ str(self.ID))

class Client:

	def __init__(self, ip, port) -> None:
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = ip
		self.port = port
		self.sockets_list = [self.server]

		# 

	# Attempts to connect to server, if no connection, query user if the want to attempt to reconnect
	def connect(self, reconnect=False):
		try:
			self.server.connect((self.IP, self.port))
			print("Client connected to the server")
			t = thread(self.wait_for_response, 0)
			t.start()			

			return True

		except ConnectionRefusedError:
			clear()
			print("Client could not connect to server...")
			if not reconnect:
				print("Connection Aborted")
				exit(0)

			return False

	
	def wait_for_response(self):
		while True:
			msg = self.server.recv(16)
			print(msg)


	def send(self, msg):
		self.server.send(bytes("test", "utf-8"))

	
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

