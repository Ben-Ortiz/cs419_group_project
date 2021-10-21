import sys



if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
IP = str(sys.argv[1]) 
port = int(sys.argv[2])
