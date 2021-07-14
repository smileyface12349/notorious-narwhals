import curses
import time
from os import get_terminal_size
from typing import NoReturn

from datatypes import Menu, Size

from .input_getter import InputGetter
from .window_manager import WindowManager


def center(string: str, width: int) -> str:
    """Center the string"""
    return f"{string:^{width}}"


class MenuDrawer:
    """A class to draw menus"""

    def __init__(self, screen: curses.window, window_manager: WindowManager, input_getter: InputGetter):
        """Initilize a new menu"""
        self.screen = screen
        self.window_manager = window_manager
        self.input_getter = input_getter
        self.width, self.height = get_terminal_size()
        curses.init_pair(1001, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1002, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def update(self) -> NoReturn:
        """Update width and height"""
        self.width, self.height = get_terminal_size()

    def draw_menu(self, menu: Menu) -> int:
        """Draw a menu"""
        self.update()
        max_lenth = max(list(map(lambda x: len(str(x)), menu.text_lines + menu.options)))
        self.window_manager.min_size = Size(
            max_lenth * self.window_manager.font_size.width,
            (len(menu.text_lines) + len(menu.options) + 3) * self.window_manager.font_size.height,
        )
        top_line = int(self.height / 2 - (len(menu.text_lines) + len(menu.options) + 3) / 2)
        return top_line  # Not done yet


class GameLoop:
    """Main game loop class. Entry point of the game."""

    def __init__(self, max_fps: int = 20):
        self.max_fps = max_fps
        self.window_manager = None
        self.active_state_box = None

        self.running = False
        self.throttle = False

    def start(self) -> NoReturn:
        """Main game loop. This method blocks until game is finished!"""
        period = 1 / self.max_fps
        self.running = True

        self._pre_loop()
        while self.running:
            frame_end_time = time.time() + period
            self._loop_step()
            sleep_time = max(0.0, frame_end_time - time.time())
            self.throttle = sleep_time == 0
            time.sleep(sleep_time)

    def _pre_loop(self) -> NoReturn:
        """Every call that is to be scheduled before loop start goes here"""
        self.window_manager.update()  # for correct population of previous frame

    def _loop_step(self) -> NoReturn:
        """Every call that is to be scheduled at each frame goes here"""
        self.window_manager.update()
        self.active_state_box.render()


if __name__ == "__main__":
    loop = GameLoop()
    loop.start()
