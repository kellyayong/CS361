# Author: Kelly Yong

from command import Command
import json


# Return to home page
def return_home():
    input("Press ENTER to return to home page... ")


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


# Add Session Feature
def add_session(session_list):
    f = open('database.txt', 'a', encoding="utf-8")
    f.write(str(session_list))
    f.write("\n")
    f.close()


# Add Prompt for details
def add_prompt():
    """Get input for add session from user"""
    date_input = str(input("Date of session (format - mm/dd/yyyy): "))
    time_input = str(
        input("Duration of this session (format - hr-min): "))
    productivity_input = str(
        input("Productivity of this session (int 0 (Bad...) to 5 (Great!)): "))

    session_list = [date_input, time_input, productivity_input]
    return session_list


# View All Feature
def view_all():
    f = open('database.txt', 'r', encoding="utf-8")
    for line in f:
        print(line, end='')
    f.close()


# Clear All Feature
def clear_all():
    open('database.txt', 'w').close()


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
        5: "Exit program"
    }

    # Add Options
    add_options = {
        # Description
        "Date Practiced": "Enter the date of the session in the format of 00/00/0000 [mm/dd/yyyy]",
        "Time Practiced": "Enter the duration of the session in the format of 00 00 [hr min]",
        "Productivity Rating": "Was it a productive session? 0 (Bad...) to 5 (Great!)"
    }

    # View All Options
    view_all_options = {
        # More filter options?
        1: "View all",
        2: "Return home"
    }

    # Search Options
    search_options = {
        1: "Search by date",
        2: "Search by duration",
        3: "Search by productivity",
        4: "View all",
        5: "Return home"
    }

    # Delete Options
    delete_options = {
        1: "Search by date",
        2: "Search by duration",
        3: "Search by productivity",
        4: "Clear log",
        5: "Return home"
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
                add_session(session_details)

                # Confirm add is succesful
                print("Session added!")

                # Ask to return to home page
                return_home()

            # View All
            elif user_select == valid_options[1]:
                # Display selected option title and options
                print(f"\nSelection: <<< {view_all_commands._title} >>>\n")
                view_all_commands.show_options()

                # Get user seletion
                user_select = view_all_commands.user_select()

                # Insert prompt & functions to view progress
                if user_select == list(view_all_options.keys())[0]:
                    view_all()

                # Ask to return to home page
                return_home()

            # Search
            elif user_select == valid_options[2]:
                # Display selected option title and options
                print(f"\nSelection: <<< {search_commands._title} >>>\n")
                search_commands.show_options()

                # Insert prompt & functions to search for a session

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
                if user_select == list(delete_options.keys())[3]:
                    # Warning for clear all
                    print("""
                          WARNING: Are you sure you want to clear all? 
                          Action will not be able to undo.
                          """)
                    if confirm_choice() == True:
                        # delete all
                        clear_all()
                        print("All sessions deleted")
                    else:
                        print("Action abandoned")

                 # Ask to return to home page
                return_home()

            # Exit
            elif user_select == valid_options[4]:
                # Exit program
                print("Exiting... See you soon, buddy\n\n<< Remember to practice >>\n")
                exit()

    except KeyboardInterrupt:
        print("\nExiting... Are you going to practice?\n")
        exit()
