# Author: Kelly Yong

from command import Command

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
        1: "Add new practice session",
        2: "Search for sessions",
        3: "View all past practice sessions",
        4: "Edit session",
        5: "Delete session",
        6: "Exit"
    }

    # Create commands for Home
    home_commands = Command("Home", home_options)

    # Add Options
    add_options = {
        "Date Practiced": "Enter date in the format of 00/00/0000 [mm/dd/yyyy]",
        "Time Practiced": "Enter duration in the format of 00 00 [hr min]",
        "Session Type": "Practiced a song or fundamentals? Enter 1 (song) or 2 (fundamentals)",
        "Productivity Rating": "Was it a productive session? 0 (Bad...) to 5 (Great!)"
    }

    # Create commands for Add
    add_commands = Command("Add a Session", add_options)

    # Search Options
    search_options = {
        1: "Search by date",
        2: "Search by duration",
        3: "View all",
        4: "Return home"
    }

    # Create commands for Search
    search_commands = Command("Search for Session", search_options)

    try:
        while True:
            # Show home page title and ptions and get user selection
            print(f"\n<<< {home_commands._title} >>>\n")
            print(home_commands.show_options())

            # get user selection
            user_select = home_commands.user_select()

            # Turn options into list to check for option selection
            valid_options = list(home_options.keys())

            # Add new
            if user_select == valid_options[0]:
                # Display selected option title and options
                print(f"\nSelection: <<< {add_commands._title} >>>\n")
                print(add_commands.show_options())

                # Insert prompt & functions to add session

            # Search
            elif user_select == valid_options[1]:
                # Insert prompt & functions to search session
                continue

            # View All
            elif user_select == valid_options[2]:
                # Insert prompt & functions to search session
                continue

            # Edit
            elif user_select == valid_options[3]:
                # Insert prompt & functions to edit session
                continue

            # Delete
            elif user_select == valid_options[4]:
                # Insert prompt & functions to delete session
                continue

            # Exit
            elif user_select == valid_options[5]:
                # Exit program
                print("Exiting... See you soon, buddy\n\n<< Remember to practice >>\n")
                exit()

    except KeyboardInterrupt:
        print("\nExiting... Are you going to practice?")
        exit()
