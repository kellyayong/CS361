# Author: Kelly Yong

from command import Command
import sqlite3
import os.path
import zmq


# Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


###### Database ######

# Database - create_table
def create_table():
    try:
        # Connection object
        connection = sqlite3.connect(db_path)

        # cursor object
        cursor = connection.cursor()

        # Creating table
        sessions = """CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY, 
                date DATE, 
                duration TIME, 
                productivity INTEGER
            );"""

        cursor.execute(sessions)
        connection.commit()
        print("Sessions table successfully created in database.")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to create table in database.", error)
    finally:
        if connection:
            connection.close()
            # print("The SQLite connection is closed")


# Database - add session
def add_session(session_list):
    date_input = session_list[0]
    duration_input = session_list[1]
    productivity_input = session_list[2]

    try:
        # Connection object
        connection = sqlite3.connect(db_path)
        # cursor object
        cursor = connection.cursor()
        # print("Successfully Connected to SQLite")

        count = cursor.execute("INSERT INTO sessions (session_id, date, duration, productivity) VALUES (NULL,?,?,?)",
                               (date_input, duration_input, productivity_input))
        connection.commit()
        print(
            f"\n{cursor.rowcount} Session added successfully!\n")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to add session into table! :( \n", error)
    finally:
        if connection:
            connection.close()
            # print("The SQLite connection is closed")


# View All Feature
def view_all():
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM sessions")
            rows = cursor.fetchall()
            print(f"\n<<< All Sessions >>>\n")
            for row in rows:
                print("SESSION ID: ", row[0])
                print("DATE: ", row[1])
                print("DURATION: ", row[2])
                print("PRODUCTIVITY: ", row[3])
                print("\n")
    except sqlite3.Error as e:
        print(e)


# Search session
def search_session(selection, input):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if selection == 1:
            cursor.execute("SELECT * FROM sessions WHERE date=?", (input,))
            rows = cursor.fetchall()
            for row in rows:
                # print("\n")
                print("SESSION ID: ", row[0])
                print("DATE: ", row[1])
                print("DURATION: ", row[2])
                print("PRODUCTIVITY: ", row[3])
        elif selection == 2:
            cursor.execute("SELECT * FROM sessions WHERE duration=?", (input,))
            rows = cursor.fetchall()
            for row in rows:
                # print("\n")
                print("SESSION ID: ", row[0])
                print("DATE: ", row[1])
                print("DURATION: ", row[2])
                print("PRODUCTIVITY: ", row[3])
        elif selection == 3:
            cursor.execute(
                "SELECT * FROM sessions WHERE productivity=?", (input,))
            rows = cursor.fetchall()
            for row in rows:
                # print("\n")
                print("SESSION ID: ", row[0])
                print("DATE: ", row[1])
                print("DURATION: ", row[2])
                print("PRODUCTIVITY: ", row[3])
        else:
            print("Invalid input, please try again.")
    except sqlite3.Error as e:
        print(e)
        return_home()


# Clear All data from database
def clear_all():
    try:
        connection = sqlite3.connect(db_path, isolation_level=None)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sessions")
        connection.commit()
        cursor.close()
    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


# Delete specific session from database
def delete_session(selection, input):
    try:
        # automates commits with isolation_level set to none
        connection = sqlite3.connect(db_path, isolation_level=None)
        cursor = connection.cursor()
        if selection == 1:
            cursor.execute(
                "DELETE FROM sessions WHERE date=?", (input,))
            # connection.commit()
            print("Success, session deleted!")
        elif selection == 2:
            cursor.execute("DELETE FROM sessions WHERE duration=?", (input,))
            # connection.commit()
            print("Success, session deleted!")
        elif selection == 3:
            cursor.execute(
                "DELETE FROM sessions WHERE productivity=?", (input,))
            # connection.commit()
            print("Success, session deleted!")
        else:
            print("Invalid input, please try again.")

        view_all()
        cursor.close()
    except sqlite3.Error as e:
        print(e)
        return_home()
    finally:
        if connection:
            connection.close()
            # print("The SQLite connection is closed")


# Return to home page
def return_home():
    input("\nPress ENTER to return to home page... ")


# Get confirmation
def confirm_choice():
    user_input = str(input("Type 'y' to continue, otherwise type 'n' "))
    if user_input == "y":
        return True
    elif user_input == "n":
        return False
    else:
        print("Invalid input. Please type 'y' for yes and 'n' for no")
        confirm_choice()


# Add Prompt asking for details
def add_prompt():
    """Get input for add session from user"""
    date_input = str(input("Date of session (format - YYYY-MM-DD): "))
    duration_input = str(
        input("Duration of this session (format - HH:MM:SS): "))
    productivity_input = int(
        input("Productivity of this session (int 0 (Bad...) to 5 (Great!)): "))

    session_list = [date_input, duration_input, productivity_input]
    return session_list


# Search Prompt asking for details
def search_prompt(selection):
    """Get input for the search session from user"""
    if selection == 1:
        user_input = str(input(
            "Enter date of the session (format - YYYY-MM-DD): "))
    elif selection == 2:
        user_input = str(
            input("Enter duration of the session (format - HH:MM:SS): "))
    elif selection == 3:
        user_input = int(
            input("Enter productivity of the session (int 0 (Bad...) to 5 (Great!)): "))
    return user_input


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


if __name__ == "__main__":
    # Home  - Title
    title = """
____________  ___  _____ _____ _____ _____  _____  ______ _   _______________   __
| ___ \ ___ \/ _ \/  __ \_   _|_   _/  __ \|  ___| | ___ \ | | |  _  \  _  \ \ / /
| |_/ / |_/ / /_\ \ /  \/ | |   | | | /  \/| |__   | |_/ / | | | | | | | | |\ V /
|  __/|    /|  _  | |     | |   | | | |    |  __|  | ___ \ | | | | | | | | | \ /
| |   | |\ \| | | | \__/\ | |  _| |_| \__/\| |___  | |_/ / |_| | |/ /| |/ /  | |
\_|   \_| \_\_| |_/\____/ \_/  \___/ \____/\____/  \____/ \___/|___/ |___/   \_/
"""

    subtitle = "Are you practicing your instrument? Log your sessions here."

    # Display Title & Subtitle
    print(f"{title}\n{subtitle}\n")

    # Home Page Options
    home_options = {
        1: "Add - add new practice session",
        2: "See progress - view all your past sessions",
        3: "Search session - search for a session by Date, Duration, or Productivity",
        4: "Delete session - delete a specific session or clear all",
        5: "Need Motivation? - get a random quote",
        6: "Exit program"
    }

    # Add Options
    add_options = {
        # Description
        "Date Practiced": "Enter the date of the session in the format of [YYYY-MM-DD]",
        "Time Practiced": "Enter the duration of the session in the format [HH:MM:SS]",
        "Productivity Rating": "Was it a productive session? 0 (Bad...) to 5 (Great!)"
    }

    # View All Options
    view_all_options = {
        # More options
        1: "View all",
        2: "Display table",
        3: "Graph of productivity",
        4: "Return home"
    }

    # Search Options
    search_options = {
        1: "Search by date",
        2: "Search by duration",
        3: "Search by productivity",
        4: "Return home"
    }

    # Delete Options
    delete_options = {
        1: "Search by date",
        2: "Search by duration",
        3: "Search by productivity",
        4: "Clear log",
        5: "Return home"
    }

    # Quote Options
    quote_options = {
        1: "Need some motivational quotes?",
        2: "Return home"
    }

    # Create commands for Home
    home_commands = Command("Home", home_options)

    # Create commands for Add
    add_commands = Command("Add a Session", add_options)

    # Create commands for View Progress
    view_all_commands = Command("View Progress", view_all_options)

    # Create commands for Search
    search_commands = Command("Search Session", search_options)

    # Create commands for Delete
    delete_commands = Command("Delete Session", delete_options)

    # Create commands for Quote
    quote_commands = Command("Motivational Quotes", quote_options)

    ##### Database #####

    # Create sessions database table
    create_table()

    try:
        while True:
            # Show home page title, options, and get user selection
            print(f"\n<<< {home_commands._title} >>>\n")
            home_commands.show_options()

            # get user selection
            user_select = home_commands.user_select()

            # Turn options into list to check for option selection
            valid_options = list(home_options.keys())

            # Add new
            if user_select == valid_options[0]:
                # Display selected option title and options
                print(f"\nSelection: <<< {add_commands._title} >>>\n")
                # Show descriptions
                add_commands.show_options()

                # Insert prompt & functions to add session
                session_details = add_prompt()

                # print(session_details)
                add_session(session_details)

                # Ask to return to home page
                return_home()

            # View All
            elif user_select == valid_options[1]:
                # Display selected option title and options
                print(f"\nSelection: <<< {view_all_commands._title} >>>\n")
                view_all_commands.show_options()

                # Get user seletion
                user_select = view_all_commands.user_select()

                # Option 1 - view all sessions as list
                if user_select == list(view_all_options.keys())[0]:
                    view_all()

                # Option 2 - display table with all sessions
                if user_select == list(view_all_options.keys())[1]:
                    # Assign socket
                    socket_port = "tcp://localhost:5004"

                    # Assign request message to send
                    send_msg = "display table"

                    # Connect to microservice
                    message = connect_microservice(
                        socket_port, send_msg, "string")

                    print(f"\n{message}")

                # Option 3 - view graph of productivity
                if user_select == list(view_all_options.keys())[2]:
                    # Assign socket
                    socket_port = "tcp://localhost:5002"

                    # Assign request message to send
                    send_msg = "graph productivity"

                    # Connect to microservice
                    message = connect_microservice(
                        socket_port, send_msg, "string")

                    print(message)

                # Ask to return to home page
                return_home()

            # Search
            elif user_select == valid_options[2]:
                # Display selected option title and options
                print(f"\nSelection: <<< {search_commands._title} >>>\n")
                search_commands.show_options()

                # Get user seletion
                user_select = search_commands.user_select()

                # return home if user select home
                if user_select == 4:
                    return_home()
                else:
                    # Get search input
                    search_input = search_prompt(user_select)

                    # Insert prompt & functions to search for a session
                    search_session(user_select, search_input)

                    # Ask to return to home page
                    return_home()

            # Delete
            elif user_select == valid_options[3]:
                # Display selected option title and options
                print(f"\nSelection: <<< {delete_commands._title} >>>\n")
                delete_commands.show_options()

                # Get user seletion
                user_select = delete_commands.user_select()

                # Insert prompt & functions to delete session
                if user_select == list(delete_options.keys())[4]:
                    # Ask to return to home page
                    return_home()
                elif user_select == list(delete_options.keys())[3]:
                    # Warning for clear all
                    print("""
                          WARNING: Are you sure you want to clear all? 
                          Action will not be able to undo.
                          """)
                    if confirm_choice() == True:
                        # delete all
                        clear_all()
                        print("All sessions deleted!")
                    else:
                        print("Action abandoned")
                elif user_select == list(delete_options.keys())[0] or list(delete_options.keys())[1] or list(delete_options.keys())[2]:
                    # Get search input to find which to delete
                    search_input = search_prompt(user_select)
                    print(
                        f"you have selected {user_select} and your input is {search_input}")

                    if confirm_choice() == True:
                        # Delete the searched for session
                        delete_session(user_select, search_input)
                        print("Selected sessions deleted!")
                    else:
                        print("Action abandoned")
                else:
                    # Ask to return to home page
                    return_home()

            # Quote
            elif user_select == valid_options[4]:
                # Display selected motivational quotes
                print(f"\nSelection: <<< {quote_commands._title} >>>\n")
                quote_commands.show_options()
                # Get user seletion
                user_select = quote_commands.user_select()

                # Insert prompt & functions to delete session
                if user_select == list(quote_options.keys())[0]:

                    # Assign socket
                    socket_port = "tcp://localhost:5003"

                    # Assign request message to send
                    send_msg = "motivation"
                    # send_msg = "Quote please!"

                    # Connect to microservice
                    message = connect_microservice(
                        socket_port, send_msg, "string")
                    print(message)

                    # Print Quote
                    # print(f"\n<<< {message} >>>")

                # Ask to return to home page
                return_home()

            # Exit
            elif user_select == valid_options[5]:
                # Exit program
                print("Exiting... See you soon, buddy\n\n<< Remember to practice >>\n")

                # close connection to database
                # connection.close()

                exit()

    except KeyboardInterrupt:
        print("\nExiting... Are you going to practice?\n")

        # close connection to database
        # connection.close()

        exit()
