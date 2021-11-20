# cs419 computer security group project
The messenger branch where the implementation of the sockets in python will be found.   
   
How to test:   
open 1 terminal in administrator mode and type 'ipconfig'   
note your IPv4 address   
use port 8888   
   
   
open 3 terminals     
1 terminal is for the server    
1 terminal is for the 1st client    
1 terminal is for the 2nd client    
   
in the server terminal, type "python server.py 'YOUR IPv4 address' 8888" to start the server   
   
in the 1st client terminal type "python main.py"    
a gui should pop up   
enter the username: Josh, password: password, IP Address(as before) and port(8888) for the 1st client to login   
a gui to enter who to send message to and what to send should pop up   
   
in the 2nd client terminal type "python main.py"    
a gui should pop up   
enter the username: Anthony, password: 123, IP Address(as before) and port(8888) for the 1st client to login   
a gui to enter who to send message to and what to send should pop up   
   
Now you can send messages from one to the other and the messages will appear in all terminals (server terminal, 1st client terminal and 2nd client terminal)