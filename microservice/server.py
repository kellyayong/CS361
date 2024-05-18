#
#   Personality server in Python
#   Binds REP socket to tcp://*:5555
#   Expects personality type from client, replies with personality info
#

import zmq

# Create socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def convert_file():
    # Find file with personality info
    filename = "personality_info.csv"

    # Create empty dictionary
    personality_types = {}

    # Open file
    with open(filename, 'r') as f:
        # turn file in dictionary
        for line in f:
            # Split line into key and val
            line = line.split(",", maxsplit=2)
            key = line[0]
            val = line[1].rstrip()

            # Add info for types into dictionary
            personality_types[key] = val

    # return Personality types as a dictionary
    return personality_types


def lookup(type):
    # Convert columns in file into dictionary
    personality_types_dict = convert_file()

    # Return ifo for corresponding personality type
    personality_info = personality_types_dict[type]
    return personality_info


while True:
    # Wait for next request from client
    message = socket.recv_string()

    # Will receive personality type and display
    print(f"Received request: {message}")

    # Look up info for corresponding personality type
    personality_info = lookup(message)

    #  Send reply back to client
    socket.send_string(personality_info)
