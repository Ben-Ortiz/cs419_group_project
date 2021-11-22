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
1 terminal is for the 1st client    
1 terminal is for the 2nd client    
   
in the server terminal, type "python server.py 'YOUR IPv4 address' 8888" to start the server   
   
in the 1st client terminal type "python app.py"     
type "create"
enter a username (example: alice)
enter a password (example: alice)
type "message"

in the 1st client terminal type "python app.py"     
type "create"
enter a username (example: bob)
enter a password (example: bob)
type "message"

   
Now you can send messages from one to the other and the messages will appear in all terminals (server terminal, 1st client terminal and 2nd client terminal)