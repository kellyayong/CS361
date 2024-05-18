#
#   Personality client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends personality type to server, expects personality info back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to personality lookup server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Set request as the personality type
request = "type1"

# Send request and wait for response
# print(f"Sending request {request} …")
print(f"Searching for personality {request} …")
socket.send_string(request)

# Get reply
message = socket.recv_string()
# print(f"Received reply [ {message} ]")
print(f"Your Personality type is: {request} \n [ {message} ]")
