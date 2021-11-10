import sys
from tkinter.constants import END
from messenger.client import Client

import tkinter
import tkinter.messagebox as messagebox

import csv
 


class App:

    def __init__(self) -> None:
        self.root = tkinter.Tk()
        self.root.title = "Login"
        self.login()


    def run(self):
        self.root.mainloop()


    def connect(self):

        packet = {
            "user": self.login_screen["user"]["entry"].get(),
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

        # Check uniqueness of username
        with open('data/accounts.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == packet["user"]:
                    print(f'Username found')
                    break

        # Change scene
        self.login_screen["user"]["entry"].delete(0, END)
        self.login_screen["ip"]["entry"].delete(0, END)
        self.login_screen["port"]["entry"].delete(0, END)

        self.user = packet["user"]
        self.login_screen["frame"].destroy()

        self.home()


    def login(self):

        names = ["user", "ip", "port"]
        texts = ["Username:", "IP Address:", "Port:"]


        frame = tkinter.Frame(self.root)
        self.login_screen = {
            "frame":frame
        }
        
        for i in range(len(names)):
            widget = {}
            widget["lbl"] = tkinter.Label(frame, text=texts[i])
            widget["entry"] = tkinter.Entry(frame, width=30)

            widget["lbl"].grid(row=i, column=0)
            widget["entry"].grid(row=i, column=1)

            self.login_screen[names[i]] = widget           
        
        widget = {}
        widget["bttn"] = tkinter.Button(frame, text="Add", command=self.connect)
        widget["bttn"].grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.login_screen["submit"] = widget

        frame.pack()


    def home(self):

        #TODO load new messages from messages.csv

        names = []
        texts = []

        frame = tkinter.Frame(self.root)
        self.home_screen = {
            "frame":frame
        }

        self.home_screen["user"] = tkinter.Label(frame, text=f"Username: {self.user}")
        self.home_screen["user"].grid(row=0, column=0)

        for i in range(len(names)):
            widget = {}
            widget["lbl"] = tkinter.Label(frame, text=texts[i])
            widget["entry"] = tkinter.Entry(frame, width=30)

            widget["lbl"].grid(row=i, column=0)
            widget["entry"].grid(row=i, column=1)

            self.home_screen[names[i]] = widget           
        
        widget = {}
        widget["bttn"] = tkinter.Button(frame, text="Send Message to Anthony", command=self.message_user)
        widget["bttn"].grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.home_screen["submit"] = widget

        frame.pack()


    def message_user(self):
        #TODO message a specific user using the GUI
        #TODO create (in the GUI) a list of users to message, which
        # would make the check_for_user method obsolete
        #TODO create message in the GUI

        if(self.check_for_user("Anthony")):
            # create json package which includes the sender, the recipient and the message
		    j = {
                "sender": self.username,
                "recpt": user,
                "message": msg
		    }
            self.client.send_msg(j)

    
    def check_for_user(self, user):

        """Checks database to see if account exists"""

        return True