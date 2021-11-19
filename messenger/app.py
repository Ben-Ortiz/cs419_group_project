from tkinter.constants import END
from messenger.client import Client
import tkinter as tk
import tkinter.messagebox as messagebox
from threading import Thread
from messenger import support
 


HEADER_SIZE = 10



class App:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title = "Login"
        self.login()


    def run(self):
        self.root.mainloop()


    def connect(self):

        packet = {
            "user": self.login_screen["user"]["entry"].get(),
            "password": self.login_screen["password"]["entry"].get(),
            "ip"  : self.login_screen["ip"]["entry"].get(),
            "port": self.login_screen["port"]["entry"].get()
        }

        # Attempt to connect to server
        try:
            self.client = Client(packet["user"], packet["ip"], int(packet["port"]))
            connection = self.client.connect_to_server(reconnect=True)

        except ValueError as e:
            messagebox.showinfo("Error", e)
            print(e)
            return

        # Check if connection was successful
        if not connection:
            messagebox.showinfo("Error", "Client could not connect to server")
            return

        # Check login info
        login_lib = {"type":"login_check", "src":packet["user"], "dest":"server", "data":packet["password"], "is_encrypted":False}
        if(self.client.verify_login(login_lib)):
            print(f"Successful login")
        else:
            print(f"Invalid login attempt")
            exit()

        # Change scene
        self.login_screen["user"]["entry"].delete(0, END)
        self.login_screen["ip"]["entry"].delete(0, END)
        self.login_screen["port"]["entry"].delete(0, END)

        self.user = packet["user"]
        self.login_screen["frame"].destroy()

        self.home()


    def login(self):

        names = ["user", "password", "ip", "port"]
        texts = ["Username:", "Password:", "IP Address:", "Port:"]


        frame = tk.Frame(self.root)
        self.login_screen = {
            "frame":frame
        }
        
        for i in range(len(names)):
            widget = {}
            widget["lbl"] = tk.Label(frame, text=texts[i])
            widget["entry"] = tk.Entry(frame, width=30)

            widget["lbl"].grid(row=i, column=0)
            widget["entry"].grid(row=i, column=1)

            self.login_screen[names[i]] = widget           
        
        widget = {}
        widget["bttn"] = tk.Button(frame, text="Add", command=self.connect)
        widget["bttn"].grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.login_screen["submit"] = widget

        frame.pack()


    def home(self):

        names = ["dest", "message"]
        texts = ["To:", "Message:"]

        frame = tk.Frame(self.root)
        self.home_screen = {
            "frame":frame
        }

        #self.home_screen["user"] = tk.Label(frame, text=f"Username: {self.user}")
        #self.home_screen["user"].grid(row=0, column=0)

        for i in range(len(names)):
            widget = {}
            widget["lbl"] = tk.Label(frame, text=texts[i])
            widget["entry"] = tk.Entry(frame, width=30)

            widget["lbl"].grid(row=i, column=0)
            widget["entry"].grid(row=i, column=1)

            self.home_screen[names[i]] = widget           
        
        widget = {}
        widget["bttn"] = tk.Button(frame, text="Send Message", command=self.message_user)
        widget["bttn"].grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.home_screen["submit"] = widget

        frame.pack()

        # Thread to recieve any incoming messages
        t = Thread(target=self.client.wait_and_recieve)
        t.start()


    def message_user(self):
        packet = {
            "dest": self.home_screen["dest"]["entry"].get(),
            "message": self.home_screen["message"]["entry"].get()
        }

        message_lib = {"type":"message", "src":self.user, "dest":packet["dest"], "data":packet["message"], "is_encrypted":True}
        support.send_message(message_lib, self.client.client_socket, HEADER_SIZE)