import curses
from threading import Thread
from typing import NoReturn


class InputGetter:
    """A class that uses curses.getch() to get input"""

    def __init__(self, screen: curses.window):
        """Initilize the InputGetter"""
        self.screen = screen
        self.char_index_list = []
        self.running = True
        self.thread = Thread(target=self._loop)
        self.thread.start()

    def _loop(self) -> NoReturn:
        """Main InputGetter loop (called as thread)"""
        while self.running:
            pass

    def quit(self) -> NoReturn:
        """Quit the main InputGetter loop"""
        self.running = False
