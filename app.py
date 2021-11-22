from client import Client
from threading import Thread
import os
import sys
 
IP = sys.argv[1]
PORT = int(sys.argv[2])

class App:

    def __init__(self) -> None:
        self.stack = [self.main]
        self.force_logout = False

        # clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

        while(self.stack):
            if self.force_logout:
                # Reset stack
                self.stack = [self.logout]

            # Perform action of last item on stack
            action = self.stack.pop()
            action()


    def main(self):

        while(True):
            x = input("Login or create new account? ")
            if "login".startswith(x.lower()) or "log in".startswith(x.lower()):
                self.stack.append(self.login)
                break
            if "create new account".startswith(x.lower()) or "new account".startswith(x.lower()):
                self.stack.append(self.new_account)
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
            self.ip = IP
            self.port = PORT


            if not self.connect():
                while(True):
                    retry = input("Try again? (y/n) ")
                    if retry == 'y':
                        break
                    if retry == 'n':
                        print("\n")
                        self.stack.append(self.main)
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
                        self.stack.append(self.main)
                        return
                    else:
                        print("Invalid input")

                continue
    
        self.stack.append(self.home)
        self.stack.append(self.start_thread)


    def new_account(self):

        print("\n")
        
        while(True):
            self.user = input("Username: ")
            password = input("Password: ")
            #self.ip = input("IP address: ")
            #self.port = int(input("Port: "))
            self.ip = IP
            self.port = PORT

            if not self.connect():
                while(True):
                    retry = input("Try again? (y/n) ")
                    if retry == 'y':
                        break
                    if retry == 'n':
                        print("\n")
                        self.stack.append(self.main)
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
                        self.stack.append(self.main)
                        return
                    else:
                        print("Invalid input")

                continue

        self.stack.append(self.home)
        self.stack.append(self.start_thread)


    def start_thread(self):
        self.t = Thread(target=self.recieve_messages)
        self.t.start()


    def recieve_messages(self):
        self.client.wait_and_recieve()

        self.force_logout = True


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
                self.stack.append(self.home)
                self.stack.append(self.message_user)
                break

            if "conversation".startswith(x.lower()):
                self.stack.append(self.home)
                self.stack.append(self.show_messages)
                break

            if "remove".startswith(x.lower()) and admin:
                self.stack.append(self.home)
                self.stack.append(self.remove_user)
                break

            if "logout".startswith(x.lower()) or "log out".startswith(x.lower()):
                self.stack.append(self.logout)
                break

            else:
                print("Command undefined.")


    def message_user(self):
        user = input("Send to: ")
        message = input("Enter your message.\n")

        self.client.send_message(user, message)


    def show_messages(self):
        user = input("See conversation with: ")

        self.client.get_messages(user)

        self.stack.append(self.home)


    def remove_user(self):
        return True


    def logout(self):

        print("Logging out...\n")

        #TODO send message to server to log user out

        # Join thread
        if self.t.is_alive():
            self.t.join()

        self.stack.append(self.main)
        self.force_logout = False


    
if __name__ == "__main__":
    app = App()
