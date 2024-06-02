import zmq
import sqlite3
import os.path
from tkinter import ttk
import tkinter as tk

# Create context
context = zmq.Context()

# Create socket
socket = context.socket(zmq.REP)

# Bind socket to main program
socket.bind("tcp://localhost:5004")

# Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'app', "database.db")


def View():
    con1 = sqlite3.connect(db_path)
    print(db_path)
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM sessions")
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values=row)
    con1.close()


while True:
    request = socket.recv_string()
    print("Received request: %s" % request)
    if request == "display table":
        # Main tkinter window
        root = tk.Tk()

        # Set title
        root.title('Productivity Graph')

        # Set up table
        tree = ttk.Treeview(root, column=(
            "c1", "c2", "c3", "c4"), show='headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text="Session ID")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="Date")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="Duration")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text="Productivity")
        tree.pack()

        # Display data
        view_button = tk.Button(text="Display data", command=View)
        view_button.pack(pady=10)
        root.mainloop()

    socket.send_string("Table displayed")
    print("Request sent")
