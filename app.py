from client import Client
from threading import Thread
import os
 


HEADER_SIZE = 10



class App:

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
                print("Try again")
                continue

            # Check login info
            
            if(self.client.verify_login(self.user, password)):
                print("Successfully logged in")
                break
            else:
                print("Invalid login attempt, try again")
                continue

        self.home(self)


    def new_account(self):

        print("\n")
        
        while(True):
            self.user = input("Username: ")
            password = input("Password: ")
            self.ip = input("IP address: ")
            self.port = int(input("Port: "))

            if not self.connect(self): continue

            if self.client.create_account(self.user, password):
                print("Successfully created account")
                break
            else:
                print("Could not create account. Your username may already exist.")
                continue

        self.home(self)


    def home(self):

        print("\n")

        # Thread to recieve any incoming messages
        t = Thread(target=self.client.wait_and_recieve)
        t.start()

        print("Message a user: message")
        print("Show conversation with a user: conversation")
        print("Logout: logout")

        while(True):
            x = input()
            if "message".startswith(x.lower()):
                self.message_user(self)

            if "conversation".startswith(x.lower()):
                self.show_messages(self)

            if "logout".startswith(x.lower()) or "log out".startswith(x.lower()):
                self.logout(self)


    def message_user(self):
        user = input("Send to: ")
        message = input("Enter your message.\n")

        self.client.send_message(user, message)


    def show_messages(self):
        user = input("See conversation with: ")

        


    def logout(self):
        return True


    
if __name__ == "__main__":
    # clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    while(True):
        x = input("Login or create new account? ")
        if "login".startswith(x.lower()) or "log in".startswith(x.lower()):
            action = App.login
            break
        if "new account".startswith(x.lower()):
            action = App.new_account
            break
        else:
            print("\nInvalid inpout, please try again.\n")

    action(App)