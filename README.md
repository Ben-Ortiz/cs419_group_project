# cs419 computer security group project

[google docs](https://docs.google.com/document/d/15hVa0cmSZLMbEvgxXL2C6mP6GTozdQyf7S_c2eYLCLU/edit?usp=sharing)

What we need to do (according to slides):  
- [x] Project Topic: Due 9/23/2021 11:59pm  
- [x] Midterm Report: Due 10/28/2021 11:59pm    
- [ ] Code Freeze: Due 11/21/2021    
- [ ] Presentation: Due last few weeks  
- [ ] Final Report: Due final week of semester  
  
Note: Code freeze and presentation will be announced after midterm report

How to test this:   
open 1 terminal in administrator mode and type 'ipconfig'   
note your IPv4 address   
use port 8888   
   
open 3 terminals     
1 terminal is for the server    
1 terminal is for the 1st app    
1 terminal is for the 2nd app    
   
in the server terminal, type "python server.py 'YOUR IPv4 address' 8888" to start the server   
   
in the 1st app terminal type "python app.py 'YOUR IPv4 address' 8888" to start the 1st app     
type "create"   
enter a username (example: alice)   
enter a password (example: alice)   
type "message"   
a prompt "Send to:" will show on the terminal   
enter bob   
a prompt "Enter your message." will show on the terminal   
type your message (example: hi)   
that message should show up on bob's terminal   
to see the conversation between alice and bob type "conversation"   
to logout type "logout"   
   
in the 2nd app terminal type "python app.py 'YOUR IPv4 address' 8888" to start the 2nd app          
type "create"   
enter a username (example: bob)   
enter a password (example: bob)   
type "message"   
a prompt "Send to:" will show on the terminal   
enter bob   
a prompt "Enter your message." will show on the terminal   
type your message (example: hi)   
that message should show up on alice's terminal   
to see the conversation between alice and bob type "conversation"   
to logout type "logout"   


To use this from two different computers port forwarding has to be enabled for both computers.   
This poses a security risk, be warned. 