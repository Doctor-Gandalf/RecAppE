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

    def add_recipe(self, filename):
        """Load a recipe and add it to the shopping list.

        :param filename: the recipe (located in saved_recipes) to be loaded
        :return: null
        """
        # Add the directory name to the filename.
        filename = 'saved_recipes/' + filename

        # Handle error in case file doesn't exist.
        try:
            new_recipe = Recipe.create_from_file(filename)
            # Add ingredients to the shopping list.
            new_recipe.add_to(self._shopping_list)

            # Alert user that list was updated.
            self._list_display.addstr(self._list_height-2, 1, "{} fully loaded".format(filename))
            self._list_display.refresh()
        except FileNotFoundError:
            # Alert user that file was not found.
            self._list_display.addstr(self._list_height-2, 1, "File not found.")
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

    def load_list(self):
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
        :return: a reference to the recipe
        """
        key = self._list_display.getkey()
        if key == '\n':
            # Shopping list is already empty so program can continue
            return self
        elif key == 'l':
            # Load a shopping list from saves.
            self.load_list()
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
        """Clear the contents of the screen."""
        self._list_display.clear()
        util.color_box(self._list_display, 0, 0, self._list_height-1, self._list_width-1, 3)
        self._list_display.refresh()
        return self

    def show_list(self):

        pass
