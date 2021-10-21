from tkinter import *

root = Tk()
root.title("Messenger App")
root.geometry("400x400")

vertical = Scale(root, from_=0, to=200)
vertical.pack(side=RIGHT)

vertical.get()

root.mainloop()