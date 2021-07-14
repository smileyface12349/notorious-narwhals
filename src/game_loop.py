import curses
import os
import time
from os import get_terminal_size
from typing import NoReturn

from datatypes import Menu, Size
from input_getter import InputGetter
from window_manager import WindowManager


def center(string: str, width: int) -> str:
    """Center the string"""
    return f"{string:^{width}}"


class MenuDrawer:
    """A class to draw menus"""

    def __init__(
        self, screen: curses.window, window_manager: WindowManager, input_getter: InputGetter, max_fps: int = 20
    ):
        """Initilize a new menu"""
        self.screen = screen
        self.window_manager = window_manager
        self.input_getter = input_getter
        self.width, self.height = get_terminal_size()
        curses.init_pair(200, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.window_manager.update()
        self.max_fps = max_fps

    def update(self) -> NoReturn:
        """Update width and height"""
        self.width, self.height = get_terminal_size()

    def draw_menu(self, menu: Menu) -> int:
        """Draw a menu"""
        max_lenth = max(list(map(lambda x: len(x), menu.text_lines + menu.options)))
        self.window_manager.min_size = Size(
            max_lenth * self.window_manager.font_size.width,
            (len(menu.text_lines) + len(menu.options) + 3) * self.window_manager.font_size.height,
        )
        self.window_manager.update()
        top_line = int(self.height / 2 - (len(menu.text_lines) + len(menu.options) + 3) / 2)
        selected = 0
        while True:
            self.update()
            self.screen.clear()
            for index, item in enumerate(menu.text_lines):
                self.screen.addstr(top_line + index + 1, 0, center(item, self.width))
            for index, item in enumerate(menu.options):
                if index == selected:
                    self.screen.attron(curses.color_pair(1000))
                self.screen.addstr(top_line + len(menu.text_lines) + index + 2, 0, center(item, self.width))
                if index == selected:
                    self.screen.attroff(curses.color_pair(1000))
            time.sleep(1 / self.max_fps)
            for key in self.input_getter.get_char_index_iterator(clear=True):
                if key == 10:
                    return selected
                elif key == curses.KEY_UP:
                    selected = max(selected - 1, 0)
                elif key == curses.KEY_DOWN:
                    selected = min(selected + 1, len(menu.options) - 1)


class GameLoop:
    """Main game loop class. Entry point of the game."""

    def __init__(self, window_manager: WindowManager, max_fps: int = 20):
        self.max_fps = max_fps
        self.window_manager = window_manager
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


# fmt: off
menus = {
    "start": Menu(
        ["Title of the Game", "By the Notorious Narwhals"],
        ["Play", "Select Level", "How to play", "About", "Settings", "Exit"],
    ),
    "levels": Menu(
        ["Not implemented yet"],
        ["Back"]
    ),
    "help": Menu(
        ["Paste here a nice explanation", "how to play the game"],
        ["Back"]
    ),
    "about": Menu(
        ["Paste here a nice text about", "hte Notorious Narwhals and the Code Jam"],
        ["Back"]
    ),
    "settings": Menu(
        ["Not implemented yet"],
        ["Back"]
    ),
}
# fmt: on


def main(screen: curses.window) -> NoReturn:
    """Main curses function"""
    curses.curs_set(False)
    os.environ.setdefault("ESCDELAY", "25")

    window_manager = WindowManager()
    input_getter = InputGetter(screen)
    menu_drawer = MenuDrawer(screen, window_manager, input_getter)

    menu = "start"
    while True:
        menu_return = menu_drawer.draw_menu(menus[menu])
        if menu == "start":
            if menu_return == 0:
                break
            elif menu_return == 1:
                menu = "levels"
            elif menu_return == 2:
                menu = "help"
            elif menu_return == 3:
                menu = "about"
            elif menu_return == 4:
                menu = "settings"
            elif menu_return == 5:
                return
        elif menu in ["levels", "help", "about", "settings"]:
            menu = "start"

    loop = GameLoop(window_manager)
    loop.start()


if __name__ == "__main__":
    curses.wrapper(main)
