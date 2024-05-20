from tkinter import *
from tkinter import ttk
root = Tk()
root.title("Main Window")
root.minsize(800,400)
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()