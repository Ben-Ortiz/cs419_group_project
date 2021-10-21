import sys
from messenger.client import Client


if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
IP = str(sys.argv[1]) 
port = int(sys.argv[2])

c = Client(IP, port)

r = True
connected = c.connect(r)
while not connected:
    if r:
        r = input("Do you want to attempt reconnect? (y/n) > ") == "y"
    connected = c.connect(r)
    
    



