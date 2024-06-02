import zmq
import tkinter as tk


# Create context
context = zmq.Context()

# Create socket
socket = context.socket(zmq.REP)

# Bind socket to main program
socket.bind("tcp://localhost:5003")


### Connect to Microservice ###
def connect_microservice(socket_port, send_msg, send_type):
    # Create context
    context = zmq.Context()

    # Create socket
    socket = context.socket(zmq.REQ)
    socket.connect(socket_port)

    if send_type == "string":
        # Send request
        socket.send_string(send_msg)
    elif send_type == "b":
        socket.send(b'send_msg')

    # Receive
    message = socket.recv_string()

    # Return message
    return message


def get_quote():
    # Assign socket
    socket_port = "tcp://localhost:5001"

    # Assign request message to send
    send_msg = "Quote please!"

    # Connect to microservice
    quote = connect_microservice(socket_port, send_msg, "b")

    # Update quote
    my_var.set(quote)

   # return quote


while True:
    request = socket.recv_string()
    print("Received request: %s" % request)
    if request == "motivation":

        # Main tkinter window
        window = tk.Tk()

        # Set title
        window.title('Motivational Quote')

        # setting dimensions of window
        window.geometry("500x400")

        my_var = tk.StringVar()
        my_var.set("Click on button to get a motivational quote :)")

        # Create a label widget
        label = tk.Label(window, textvariable=my_var, bg="black",
                         fg="white", relief="groove", text="longtext",
                         anchor="center", justify="left", wraplength=250,
                         width=100, height=15)

        # Create a button widget
        quote_button = tk.Button(window, text="New Quote", command=get_quote)

        # place button and label in window
        quote_button.pack(pady=20)
        label.pack(padx=50, pady=20)

        # run the gui
        window.mainloop()

    socket.send_string("Graphed Productivity")
    print("Request sent")
