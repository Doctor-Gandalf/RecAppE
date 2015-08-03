__author__ = 'Kellan Childers'

import curses
from recipe import Recipe


class MainScreen:
    def __init__(self):
        self._shopping_list = Recipe()
