import sys
from messenger import client
from messenger.client import Client

from messenger.app import App

client = App()

client.run()



exit(0)




if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
IP = str(sys.argv[1]) 
port = int(sys.argv[2])

c = Client(IP, port)

r = True
while r:
    connected = c.connect(r)
    if connected:
        break
    r = input("Do you want to attempt reconnect? (y/n) > ") == "y"


while True:
    c.query_server()

c.close()

    
    
    



