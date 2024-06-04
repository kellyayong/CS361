import zmq
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk


# Create context
context = zmq.Context()

# Create socket
socket = context.socket(zmq.REP)

# Bind socket to main program
socket.bind("tcp://localhost:5002")


def Graph():
    try:
        # Open database
        conn = sqlite3.connect("../app/database.db")
        sql = """SELECT date, productivity FROM sessions GROUP BY date"""
        data = pd.read_sql(sql, conn)
        ax = plt.subplot()
        ax.bar(data.date, data.productivity, color='grey',
               width=0.2)
        ax.set_title('Productivity of Practice Session')
        ax.set_xlabel('Dates')
        ax.set_ylabel('Productivity')

        plt.show()

    except sqlite3.Error as e:
        # If error
        print("Error connecting to database:", e)
    conn.close()


while True:
    request = socket.recv_string()
    print("Received request: %s" % request)
    if request == "graph productivity":
        # Main tkinter window
        window = tk.Tk()

        # Set title
        window.title('Productivity Graph')

        # setting the dimensions of
        # the main window
        window.geometry("300x300")

        # Set up button
        graph_button = tk.Button(text="Graph", command=Graph)

        # place button in window
        graph_button.pack(pady=10)

        # run the gui
        window.mainloop()

    socket.send_string("Graphed productivity")
    print("Request sent")
