from client import Client
from threading import Thread
import os
 


HEADER_SIZE = 10



class App:

    def main(self):

        while(True):
            x = input("Login or create new account? ")
            if "login".startswith(x.lower()) or "log in".startswith(x.lower()):
                stack.append(self.login)
                break
            if "create new account".startswith(x.lower()) or "new account".startswith(x.lower()):
                stack.append(self.new_account)
                break
            else:
                print("\nInvalid inpout, please try again.\n")


    def connect(self):

        print("\n")

        # Attempt to connect to server
        try:
            self.client = Client(self.user, self.ip, self.port)
            connection = self.client.connect_to_server(reconnect=True)

        except:
            return False

        # Check if connection was successful
        if not connection:
            return False

        return True


    def login(self):

        print("\n")

        while True:
            self.user = input("Username: ")
            password = input("Password: ")
            #self.ip = input("IP address: ")
            #self.port = int(input("Port: "))
            self.ip = "10.0.0.63"
            self.port = 8888

            if not self.connect(self):
                while(True):
                    retry = input("Try again? (y/n) ")
                    if retry == 'y':
                        break
                    if retry == 'n':
                        print("\n")
                        stack.append(self.main)
                        return
                    else:
                        print("Invalid input")

                continue

            # Check login info
            
            if(self.client.verify_login(self.user, password)):
                print("Successfully logged in")
                break
            else:
                while(True):
                    retry = input("Invalid login attempt, try again? (y/n) ")
                    if retry == 'y':
                        break
                    if retry == 'n':
                        print("\n")
                        stack.append(self.main)
                        return
                    else:
                        print("Invalid input")

                continue
    
        stack.append(self.home)
        stack.append(self.recieve_messages)


    def new_account(self):

        print("\n")
        
        while(True):
            self.user = input("Username: ")
            password = input("Password: ")
            #self.ip = input("IP address: ")
            #self.port = int(input("Port: "))
            self.ip = "10.0.0.63"
            self.port = 8888

            if not self.connect(self):
                while(True):
                    retry = input("Try again? (y/n) ")
                    if retry == 'y':
                        break
                    if retry == 'n':
                        print("\n")
                        stack.append(self.main)
                        return
                    else:
                        print("Invalid input")

                continue

            if self.client.create_account(self.user, password):
                print("Successfully created account")
                break
            else:
                while(True):
                    retry = input("Failed to create account. Your username may already be taken. Try again? (y/n) ")
                    if retry == 'y':
                        break
                    if retry == 'n':
                        print("\n")
                        stack.append(self.main)
                        return
                    else:
                        print("Invalid input")

                continue

        stack.append(self.home)
        stack.append(self.recieve_messages)


    def recieve_messages(self):
        # Thread to recieve any incoming messages
        t = Thread(target=self.client.wait_and_recieve)
        t.start()


    def home(self):

        print("\n")

        admin = self.user == "Admin"

        print("Message a user: message")
        print("Show conversation with a user: conversation")
        if admin:
            print("Remove a user: remove")
            print("Reset all accounts: reset")
        print("Logout: logout")

        while(True):
            x = input()
            if "message".startswith(x.lower()):
                stack.append(self.home)
                stack.append(self.message_user)
                break

            if "conversation".startswith(x.lower()):
                stack.append(self.home)
                stack.append(self.show_messages)
                break

            if "remove".startswith(x.lower()) and admin:
                stack.append(self.home)
                stack.append(self.remove_user)
                break

            if "logout".startswith(x.lower()) or "log out".startswith(x.lower()):
                stack.append(self.logout)
                break

            else:
                print("Command undefined.")


    def message_user(self):
        user = input("Send to: ")
        message = input("Enter your message.\n")

        self.client.send_message(user, message)


    def show_messages(self):
        user = input("See conversation with: ")

        #TODO finish this


    def remove_user(self):
        return True


    def logout(self):
        return True


    
if __name__ == "__main__":
    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    stack = [App.main]
    while(stack):
        #Perform action of last item on stack
        action = stack.pop()
        action(App)