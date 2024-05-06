
class Command:
    def __init__(self, title, options={}):
        super().__init__()
        self._title = title
        self._options = options

    def show_options(self):
        for key in self._options.keys():
            print(f"{key} - {self._options[key]}\n")

    # Get user input and check if selection if valid
    def user_select(self):
        # Get max and min range - get key using dictionary indexing
        min_option = list(self._options.keys())[0]
        max_option = list(self._options.keys())[-1]

        # Verify if input is valid
        while True:
            try:
                user_select = int(
                    input("Input your selection and press ENTER: "))
                if min_option < user_select > max_option:
                    raise ValueError
            except ValueError:
                print(
                    f"Oops! That was not a valid option. Please select from {min_option} to {max_option}")
                continue
            else:
                return user_select
