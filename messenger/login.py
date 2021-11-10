import sys
from tkinter.constants import END
from messenger.client import Client
import tkinter
import tkinter.messagebox as messagebox
import csv



class Login:    
    
    def __init__(self):

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