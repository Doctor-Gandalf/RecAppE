__author__ = 'Kellan Childers'

import curses
import util
from recipe import Recipe


class MainScreen:
    def __init__(self, console_height, console_width):
        self._list_height, self._list_width = console_height-2, console_width-2
        display_start_y, display_start_x = util.center_start(console_height, console_width,
                                                             self._list_height, self._list_width)
        self._shopping_list = Recipe()
        self._list_display = curses.newwin(self._list_height, self._list_width, display_start_y, display_start_x)
        self._list_display.bkgd(' ', curses.color_pair(1))
        util.color_box(self._list_display, 0, 0, self._list_height-1, self._list_width-1, 3)

    def add_recipe(self, filename):
        filename = 'saved_recipes/' + filename
        try:
            new_recipe = Recipe.create_from_file(filename)
            for ingredient, full_quantity in new_recipe.items():
                self._shopping_list.add_ingredient(ingredient, full_quantity[0], full_quantity[1])
            self._list_display.addstr(self._list_height-2, 1, "{} fully loaded".format(filename))
        except FileNotFoundError:
            self._list_display.addstr(self._list_height-2, 1, "File not found.")
            self._list_display.refresh()

    def add_item(self, name, quantity, qualifier):
        self._shopping_list.add_ingredient(name, quantity, qualifier)
        return self._shopping_list

    def save_list(self, filename):
        data_name = 'shopping_lists/data/' + filename
        filename = 'shopping_lists/' + filename
        self._shopping_list.save_as_list(filename)
        self._shopping_list.save_to_file(data_name)

    def show_intro(self):
        """Show welcome text."""
        # Calling util.center_start using the length of the string will center the string.
        line_1_y, line_1_x = util.center_start(self._list_height-2, self._list_width-2, 1, 18)
        self._list_display.addstr(line_1_y, line_1_x, "Welcome to RecAppE")

        line_2_y, line_2_x = util.center_start(self._list_height-2, self._list_width-2, 1, 42)
        self._list_display.addstr(line_2_y+1, line_2_x, "To create a new shopping list, press enter")

        line_3_y, line_3_x = util.center_start(self._list_height-2, self._list_width-2, 1, 52)
        self._list_display.addstr(line_3_y+2, line_3_x, "To add to a previously made shopping list, press 'l'")

        line_4_y, line_4_x = util.center_start(self._list_height-2, self._list_width-2, 1, 30)
        self._list_display.addstr(line_4_y+3, line_4_x, "To quit, press 'q' at any time")

        self._list_display.refresh()
