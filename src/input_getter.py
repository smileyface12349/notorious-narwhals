import curses
from threading import Thread
from typing import NoReturn, Optional


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
            self.char_index_list.append(self.screen.getch())

    def quit(self) -> NoReturn:
        """Quit the main InputGetter loop"""
        self.running = False

    def clear(self) -> NoReturn:
        """Clear the char_index_list"""
        self.char_index_list = []

    def get_first_char_index(self, remove: bool = False, clear: bool = False) -> Optional[int]:
        """Get the first (oldest) char_index the main loop got

        If remove is true: get the first char_index and remove it from the list
        If clear is true: get the first char_index and clear the list
        If char_index_list is empty: return None
        """
        if len(self.char_index_list) == 0:
            return None
        output = self.char_index_list[0]
        if remove:
            self.char_index_list.pop(0)
        if clear:
            self.clear()
        return output

    def get_first_char(self, remove: bool = False, clear: bool = False) -> Optional[str]:
        """Get the first (oldest) char the main loop got

        If remove is true: get the first char and remove it from the list
        If clear is true: get the first char and clear the list
        If char_index_list is empty: return None
        """
        if len(self.char_index_list) == 0:
            return None
        output = str(chr(self.char_index_list[0]))
        if remove:
            self.char_index_list.pop(0)
        if clear:
            self.clear()
        return output

    def get_last_char_index(self, remove: bool = False, clear: bool = False) -> Optional[int]:
        """Get the last (newest) char_index the main loop got

        If remove is true: get the last char_index and remove it from the list
        If clear is true: get the last char_index and clear the list
        If char_index_list is empty: return None
        """
        if len(self.char_index_list) == 0:
            return None
        output = self.char_index_list[-1]
        if remove:
            self.char_index_list.pop()
        if clear:
            self.clear()
        return output

    def get_last_char(self, remove: bool = False, clear: bool = False) -> Optional[str]:
        """Get the last (newest) char the main loop got

        If remove is true: get the last char and remove it from the list
        If clear is true: get the last char and clear the list
        If char_index_list is empty: return None
        """
        if len(self.char_index_list) == 0:
            return None
        output = str(chr(self.char_index_list[-1]))
        if remove:
            self.char_index_list.pop()
        if clear:
            self.clear()
        return output
