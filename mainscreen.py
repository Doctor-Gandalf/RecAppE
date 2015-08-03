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

    def add_recipe(self, filename):
        try:
            new_recipe = Recipe.create_from_file(filename)
            for ingredient, full_quantity in new_recipe.items():
                self._shopping_list.add_ingredient(ingredient, full_quantity[0], full_quantity[1])
            self._list_display.addstr(self._list_height-1, 0, "{} fully loaded".format(filename))
        except FileNotFoundError:
            self._list_display.addstr(self._list_height-1, 0, "File not found.")
            self._list_display.refresh()

    def add_item(self, name, quantity, qualifier):
        self._shopping_list.add_ingredient(name, quantity, qualifier)
        return self._shopping_list

    def show_intro(self):
        self._list_display.addstr(0, 0, "Welcome to RecAppE")
        self._list_display.refresh()
