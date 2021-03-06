__author__ = 'Kellan Childers'

import curses
import util
from recipe import Recipe


class MainScreen:
    def __init__(self, console_height, console_width):
        """Create a main screen.

        :param console_height: the height of the console
        :param console_width: the width of the console
        :return: null
        """
        # List should be two smaller in each direction because of surrounding border.
        self._list_height, self._list_width = console_height-2, console_width-2

        # Center the window based on the size of the console.
        display_start_y, display_start_x = util.center_start(console_height, console_width,
                                                             self._list_height, self._list_width)

        # Initialize a Recipe to serve as a shopping list.
        self._shopping_list = Recipe()

        # Create window that will act as main visual.
        self._list_display = curses.newwin(self._list_height, self._list_width, display_start_y, display_start_x)

        # Add visual detail to window.
        self._list_display.bkgd(' ', curses.color_pair(1))
        util.color_box(self._list_display, 0, 0, self._list_height-1, self._list_width-1, 3)

        # Initializes help window for use in pause().
        help_height, help_width = 12, 50
        help_y, help_x = util.center_start(console_height, console_width, help_height, help_width)
        self.help_window = curses.newwin(help_height, help_width, help_y, help_x)

    def add_recipe(self, filename):
        """Load a recipe and add it to the shopping list.

        :param filename: the recipe (located in saved_recipes) to be loaded
        :return: null
        """
        # Add the directory name to the filename.
        filename = 'saved_recipes/' + filename

        new_recipe = Recipe.create_from_file(filename)
        # Add ingredients to the shopping list.
        new_recipe.add_to(self._shopping_list)

        # Alert user that list was updated.
        self._list_display.addstr(self._list_height-2, 1, "{} fully loaded".format(filename))
        self._list_display.refresh()

    def add_item(self, name, quantity, qualifier):
        """Add a single item to the shopping list.

        :param name: the name of the item
        :param quantity: the quantity of the item
        :param qualifier: the specifier of the quantity (ounces, pounds, etc)
        :return: a reference to the main screen
        """
        self._shopping_list.add_ingredient(name, quantity, qualifier)
        return self

    def remove_item(self, name):
        """Remove item from list.

        :param name: the name of the item to be removed
        :return: the removed item
        """
        return self._shopping_list.remove_ingredient(name)

    def request_element(self, request):
        """Ask for an element.

        :param request: the request for the element (requires string)
        :return: the user's response
        """
        # Clear row in preparation of getting element.
        self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))

        # Format request, then request.
        _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, len(request))
        self._list_display.addstr(self._list_height-2, line_x, request)
        self._list_display.refresh()

        # Get element.
        curses.echo()
        element = self._list_display.getstr().decode(encoding="utf-8")
        curses.noecho()

        return element

    def save_list(self, filename):
        """Save a copy of the shopping list for both user and computer use.

        Data will be saved to shopping_lists/data as json file and to shopping_lists as human-readable list.
        :param filename: the name of the file to save
        :return: a reference to the main screen
        """
        # Add appropriate directory name for each place to save.
        data_name = 'shopping_lists/data/' + filename
        filename = 'shopping_lists/' + filename

        # Save twice to allow reference later on.
        self._shopping_list.save_as_list(filename)
        self._shopping_list.save_to_file(data_name)

        return self

    def save_as_recipe(self, filename):
        """Save a copy of the shopping list for both user and computer use.

        Data will be saved to shopping_lists/data as json file and to shopping_lists as human-readable list.
        :param filename: the name of the file to save
        :return: a reference to the main screen
        """
        # Add appropriate directory name to save as recipe.
        filename = 'saved_recipes/' + filename

        # Save as a recipe.
        self._shopping_list.save_to_file(filename)

        return self

    def start_load(self):
        """Loads a list from a file.

        :return: null
        """
        # Request filename.
        line_y, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 16)
        self._list_display.addstr(line_y+4, 1, ' '*(self._list_width-2))
        self._list_display.addstr(line_y+4, line_x, "Enter filename: ")
        self._list_display.refresh()

        # Get filename
        curses.echo()
        filename = self._list_display.getstr().decode(encoding="utf-8")
        filename = 'shopping_lists/data/' + filename
        curses.noecho()

        # Try to load list, and recursively call start_command if the file isn't loaded.
        try:
            new_list = Recipe.create_from_file(filename)
            # Add ingredients to the shopping list.
            new_list.add_to(self._shopping_list)

            # Alert user that list was updated..
            line_y, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, len(filename)+13)
            self._list_display.addstr(line_y+5, line_x, "{} fully loaded".format(filename))
            self._list_display.refresh()
        except (FileNotFoundError, IsADirectoryError):
            # Alert user that file was not found.
            line_y, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 13)
            self._list_display.addstr(line_y+5, line_x, "File not found.")
            self._list_display.refresh()

            # Retry getting a command
            self.start_shopping_list()

    def show_intro(self):
        """Show welcome text."""
        # Calling util.center_start using the length of the string will center the string.
        # Line length acquired by adding str(len(...)) around text and running program.
        line_1_y, line_1_x = util.center_start(self._list_height-2, self._list_width-2, 1, 18)
        self._list_display.addstr(line_1_y, line_1_x, "Welcome to RecAppE")

        line_2_y, line_2_x = util.center_start(self._list_height-2, self._list_width-2, 1, 42)
        self._list_display.addstr(line_2_y+1, line_2_x, "To create a new shopping list, press enter")

        line_3_y, line_3_x = util.center_start(self._list_height-2, self._list_width-2, 1, 52)
        self._list_display.addstr(line_3_y+2, line_3_x, "To add to a previously made shopping list, press 'l'")

        line_4_y, line_4_x = util.center_start(self._list_height-2, self._list_width-2, 1, 30)
        self._list_display.addstr(line_4_y+3, line_4_x, "To quit, press 'q' at any time")

        self._list_display.refresh()

    def start_shopping_list(self):
        """Start the main screen by getting a command from a key.

        Pressing 'q' will quit app.
        :return: a reference to the main screen
        """
        key = self._list_display.getkey()
        if key == '\n':
            # Shopping list is already empty so program can continue
            return self
        elif key == 'l':
            # Load a shopping list from saves.
            self.start_load()
            return self
        elif key == 'q':
            # quit app.
            exit()
        else:
            # Use same method for centering text as show_intro(); add text below show_intro()'s.
            line_y, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 28)
            self._list_display.addstr(line_y+4, line_x, "Command not found, try again")

            self._list_display.refresh()
            self.start_shopping_list()

    def clear_screen(self):
        """Clear the contents of the screen.

        :return: a reference to the main screen
        """
        self._list_display.clear()

        # Add back border and show display
        util.color_box(self._list_display, 0, 0, self._list_height-1, self._list_width-1, 3)
        self._list_display.refresh()

        return self

    def show_list(self):
        """Display the shopping list on screen."""
        # Format the rows and columns the chart.
        row = 2
        column = 0

        # Set up chart header.
        _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 14)
        self._list_display.addstr(1, line_x, "Shopping list:")

        for ingredient in sorted(self._shopping_list):
            # Format where to place each element in chart.
            start_y = row
            start_x = column*20+1

            # Truncate ingredient if longer than 18 characters.
            full_ingredient = self._shopping_list.show_ingredient(ingredient)
            truncated_ingredient = full_ingredient[:18] + (full_ingredient[18:] and '..')

            # Keep printing until list runs out of space.
            try:
                self._list_display.addstr(start_y, start_x, truncated_ingredient)
            except curses.error:
                # Window has run out of room, so stop printing.
                break

            row += 1

            # Every column, restart row number.
            if row == self._list_height-2:
                column += 1
                row = 2

        self._list_display.refresh()

    def help(self):
        """Show help window."""
        self.help_window.bkgd(' ', curses.color_pair(0))

        self.help_window.addstr(1, 19, "Help window")
        self.help_window.addstr(3, 12, "To add an item, press 'a'")
        self.help_window.addstr(4, 11, "To remove an item, press 'r'")
        self.help_window.addstr(5, 11, "To load a recipe, press 'l'")
        self.help_window.addstr(6, 10, "To save as a recipe, press 'w'")
        self.help_window.addstr(7, 6, "To save as a shopping list, press 's'")
        self.help_window.addstr(8, 12, "To clear the list, press 'c'")
        self.help_window.addstr(9, 16, "To quit, press 'q'")
        self.help_window.addstr(10, 3, "Otherwise, press 'h' to return to application")

        self.help_window.refresh()

        # Close if user hits 'h', otherwise do the command user asks.
        key = self.help_window.getkey()
        if key == 'h':
            return
        else:
            self.do_command(key)

    def do_command(self, key=None):
        """Execute a command based on key input."""
        if key is None:
            key = self._list_display.getkey()

        # Clear line in case a previous command had written to it.
        self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))
        self._list_display.refresh()

        if key == 'l':
            # Load a recipe.
            try:
                filename = self.request_element("Enter name of recipe to load: ")
                self.add_recipe(filename)
            except (FileNotFoundError, IsADirectoryError):
                # Alert user that recipe wasn't loaded.
                _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 18)
                self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))
                self._list_display.addstr(self._list_height-2, line_x, "File not found")
                self._list_display.refresh()
                self.do_command()
        elif key == 'a':
            # Add an ingredient.
            try:
                # Pull data to add as a new ingredient.
                item_name = self.request_element("Enter name of item: ")
                item_quantity = int(self.request_element("Enter quantity of item: "))
                item_qualifier = self.request_element("Enter qualifier of item: ")

                self.add_item(item_name, item_quantity, item_qualifier)
            except ValueError:
                self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))
                _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 18)
                self._list_display.addstr(self._list_height-2, line_x, "Could not add item")
                self._list_display.refresh()
                self.do_command()
        elif key == 'q':
            # Quit app.
            exit()
        elif key == 's':
            # Save shopping list.
            try:
                filename = self.request_element("Enter name to save list as: ")
                self.save_list(filename)
            except IsADirectoryError:
                # User didn't enter file, so tell the user and retry.
                self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))

                _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 23)
                self._list_display.addstr(self._list_height-2, line_x, "File unable to be saved")

                self._list_display.refresh()
                self.do_command()
        elif key == 'w':
            # Save shopping list as a recipe.
            try:
                filename = self.request_element("Enter name to save recipe as: ")
                self.save_as_recipe(filename)
            except IsADirectoryError:
                # User didn't enter file, so tell the user and retry.
                self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))

                _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 23)
                self._list_display.addstr(self._list_height-2, line_x, "File unable to be saved")

                self._list_display.refresh()
                self.do_command()
        elif key == 'c':
            # Clear the shopping list.
            self._shopping_list.clear()
        elif key == 'r':
            # Remove item.
            try:
                item_name = self.request_element("Enter item to remove: ")
                self.remove_item(item_name)
            except ValueError:
                # Item wasn't in list, so tell the user and retry.
                self._list_display.addstr(self._list_height-2, 1, ' '*(self._list_width-2))

                _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 15)
                self._list_display.addstr(self._list_height-2, line_x, "Item not found")

                self._list_display.refresh()
                self.do_command()
        elif key == 'h':
            # Show help window
            self.help()
        else:
            # Tell the user that the key was an invalid command.
            _, line_x = util.center_start(self._list_height-2, self._list_width-2, 1, 18)
            self._list_display.addstr(self._list_height-2, line_x, "Command not found")
            self._list_display.refresh()
            self.do_command()
