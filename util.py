__author__ = 'Kellan Childers'

import curses
from math import floor


def center_start(console_height, console_width, window_height, window_width):
    """Find point to start window on center.

    :param console_height: the height of the console
    :param console_width: the width of the console
    :param window_height: the height of the window
    :param window_width: the width of the window
    :return: a tuple representing the coordinates of the start window
    """
    start_y = floor((console_height-window_height)/2)
    start_x = floor((console_width-window_width)/2)
    return start_y, start_x


def size_lim(console_height, console_width, bound_height, bound_width):
    """Limit the size of a window if the console is over a certain size.

    :param console_height: the height of the window
    :param console_width: the width of the window
    :param bound_height: the minimum height to start binding the window
    :param bound_width: the minimum width to start binding the window
    :return: a pair of dimensions for the window
    """
    y = console_height if console_height <= bound_height else floor(7*console_height/8)
    x = console_width if console_width <= bound_width else floor(7*console_width/8)
    return y, x


def color_box(window, start_y, start_x, stop_y, stop_x, color):
    """Create a border around a window in a certain color."""
    try:
        for i in range(start_y, stop_y):
            window.addstr(i, start_x, ' ', curses.color_pair(color))
            window.addstr(i, stop_x, ' ', curses.color_pair(color))
        for i in range(start_x, stop_x):
            window.addstr(start_y, i, ' ', curses.color_pair(color))
            window.addstr(stop_y, i, ' ', curses.color_pair(color))
        # for loops fail to add last element.
        window.addstr(stop_y, stop_x, ' ', curses.color_pair(color))
    except curses.error:
        # curses.error is raised at end of line and can safely be ignored.
        pass
