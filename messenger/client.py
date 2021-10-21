#Client Script
# Python program to implement client side of chat room. 
import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
IP = str(sys.argv[1]) 
port = int(sys.argv[2]) 
server.connect((IP, port)) 

while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	""" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"""
	read, write, err = select.select(sockets_list, [], []) 

	for s in read: 
		if s == server: 
			message = s.recv(2048) 
			print(message)
		else: 
			message = sys.stdin.readline() 
			server.send(message) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 


# Server (host) should have the top server script and the clients should have the client script. Both are labelled with a comment