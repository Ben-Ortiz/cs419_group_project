import sys
from tkinter.constants import END
from messenger.client import Client

import tkinter
import tkinter.messagebox as messagebox

import csv

class Home:

    def home(self):
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
        widget["bttn"] = tkinter.Button(frame, text="Test Function", command=self.test)
        widget["bttn"].grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.home_screen["submit"] = widget

        frame.pack()
