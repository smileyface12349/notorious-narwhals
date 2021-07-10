import curses
from typing import NoReturn

# Defining colors based on objects` properties
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular
curses.init_pair(2, 121, curses.COLOR_BLACK)  # Sticky
curses.init_pair(3, 111, curses.COLOR_BLACK)  # Icy (little to no friction)
curses.init_pair(4, 228, curses.COLOR_BLACK)  # Bouncy


class BoxState:
    """Defines the current state of the box. Has a render() method to display the contents"""

    def __init__(self):
        self.objects = []

    def clear(self) -> NoReturn:
        """Clears the box of all objects"""
        self.objects = []

    def add_object(self, added_object) -> NoReturn:
        """Adds an object to the objects list"""
        self.objects.append(added_object)
