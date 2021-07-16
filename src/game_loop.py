import curses
import enum
import os
import time
from abc import ABC
from typing import NoReturn, Optional

import levels as loaded_levels
from datatypes import Menu
from input_getter import InputGetter
from window_manager import WindowManager


def center(string: str, width: int) -> str:
    """Center the string"""
    return f"{string:^{width}}"


class ExitCodes(enum.IntEnum):
    """Return codes used in the AbstractAppLoop to indicate pause or app exit"""

    PAUSE = -2
    STOP = -1


class AbstractAppLoop(ABC):
    """Application loop class for curses"""

    PAUSE_KEYS = {27, ord("p"), ord("P")}
    STOP_KEYS = {3, 26, ord("q"), ord("Q")}

    def __init__(self, window_manager: WindowManager, input_getter: InputGetter, max_fps: int = 20):
        self.max_fps = max_fps
        self.window_manager = window_manager
        self.input_getter = input_getter

        self.running = False
        self.return_code = None
        self.throttle = False

    def start(self) -> Optional[int]:
        """Main game loop. This method blocks until game is finished!"""
        period = 1 / self.max_fps
        self.running = True
        exit_code = None

        self._pre_loop()
        while self.running:
            frame_end_time = time.time() + period

            exit_code = self._loop_step()
            if exit_code is not None:
                break

            sleep_time = max(0.0, frame_end_time - time.time())
            self.throttle = sleep_time == 0
            time.sleep(sleep_time)

        self._post_loop()
        return exit_code

    def _pre_loop(self) -> NoReturn:
        """Every call that is to be scheduled before loop start goes here"""
        self.window_manager.update()  # for correct population of previous frame

    def _post_loop(self) -> NoReturn:
        """Every call that is to be scheduled after loop stop goes here"""
        pass

    def _loop_step(self) -> Optional[int]:
        """Every call that is to be scheduled at each frame goes here"""
        self.window_manager.update()
        key = self.input_getter.get_first_char_index(remove=True)
        exit_code = self._get_key_action(key)
        return exit_code

    def _get_key_action(self, key: int) -> int:
        """Returns exit code or action of pressed key"""
        if key in self.PAUSE_KEYS:
            return ExitCodes.PAUSE
        elif key in self.STOP_KEYS:
            curses.endwin()
            return ExitCodes.STOP


class GameLoop(AbstractAppLoop):
    """Main game loop class. Entry point of the game."""

    def __init__(self, screen: curses.window, window_manager: WindowManager, input_getter: InputGetter):
        self.screen = screen
        super().__init__(window_manager=window_manager, input_getter=input_getter)

    def _loop_step(self) -> Optional[int]:
        """Every call that is to be scheduled at each frame goes here"""
        exit_code = super()._loop_step()
        self.box_state.update()
        self.box_state.render(screen=self.screen)
        return exit_code

    def _pre_loop(self) -> NoReturn:
        """Called before the loop starts"""
        super()._pre_loop()
        f = open("log.txt", "w")  # TODO
        f.write(str([level_name]))
        f.close()
        self.box_state = levels[level_name]


class MenuLoop(AbstractAppLoop):
    """Menu loop class. Handles both rendering and processing of the menu"""

    MENU_COLOR_PAIR = 200

    def __init__(
        self, screen: curses.window, window_manager: WindowManager, input_getter: InputGetter, max_fps: int = 20
    ):
        self.screen = screen
        self.menu = None
        self.selected_index = 0
        curses.init_pair(self.MENU_COLOR_PAIR, curses.COLOR_BLACK, curses.COLOR_WHITE)
        super().__init__(window_manager=window_manager, input_getter=input_getter, max_fps=max_fps)

    def show_menu(self, menu: Menu) -> Optional[int]:
        """Displays specified menu"""
        self.menu = menu
        return self.start()

    def _pre_loop(self) -> NoReturn:
        """Every call that is to be scheduled before loop start goes here"""
        super()._pre_loop()

    def _loop_step(self) -> Optional[int]:
        """Every call that is to be scheduled at each frame goes here"""
        exit_code = super()._loop_step()
        self.screen.clear()

        rows, cols = self.screen.getmaxyx()
        # self.screen.resize(rows, cols)
        curses.resize_term(rows, cols)  # more window glitches, less text glitches and crashes
        top_line = rows // 2 - (len(self.menu.text_lines) + len(self.menu.options)) // 2

        for index, item in enumerate(self.menu.text_lines):
            y = top_line + index + 1
            x = cols // 2 - len(item) // 2
            if len(item) < cols and y < rows - 1:
                self.screen.addstr(y, x, item)

        for index, item in enumerate(self.menu.options):
            color = curses.color_pair(0) if index != self.selected_index else curses.color_pair(self.MENU_COLOR_PAIR)
            y = top_line + len(self.menu.text_lines) + index + 2
            x = cols // 2 - len(item) // 2
            if len(item) < cols and y < rows - 1:  # checks aren't working sometimes?
                self.screen.addstr(y, x, item, color)

        self.screen.refresh()
        return exit_code

    def _post_loop(self) -> NoReturn:
        """Every call that is to be scheduled after loop stop goes here"""
        self.screen.clear()
        super()._post_loop()  # In case we implement there stuff soon

    def _get_key_action(self, key: int) -> int:
        """Returns exit code or action of pressed key"""
        if key == 10:
            return self.selected_index
        elif key == curses.KEY_UP:
            self.selected_index = max(self.selected_index - 1, 0)
        elif key == curses.KEY_DOWN:
            self.selected_index = min(self.selected_index + 1, len(self.menu.options) - 1)

        return super()._get_key_action(key)


level_name = ""
# fmt: off
levels = {
    "Static Test": loaded_levels.static_test,
}
# Add you level here
# Format: {"Display name", "Filename"}

menus = {
    "start": Menu(
        ["Title of the Game", "By the Notorious Narwhals"],
        ["Play", "How to play", "About", "Settings", "Exit"],
        ["levels", "help", "about", "settings", ExitCodes.STOP],
    ),
    "levels": Menu(
        ["Select Level"],
        list(levels.keys()) + ["Back"],
        list(map(lambda x: "level:" + str(x), levels.keys())) + ["start"],
    ),
    "help": Menu(
        ["Paste here a nice explanation", "how to play the game"],
        ["Back"],
        ["start"],
    ),
    "about": Menu(
        [
            "This game was created during the Python Summer Code Jam 2021",
            "by the Notorious Narwhals:",
            "https://github.com/artem30801",
            "https://github.com/Martysh12",
            "https://github.com/Noxmain",
            "https://github.com/SHIMI-W",
            "https://github.com/smileyface12349",
            "https://github.com/smokeythemonkey",
            "(In alphabetical order)"
        ],
        ["Back"],
        ["start"],
    ),
    "settings": Menu(
        ["Not implemented yet"],
        ["Back"],
        ["start"],
    ),
    "settings_paused": Menu(
        ["Not implemented yet"],
        ["Back"],
        ["pause"],
    ),
    "pause": Menu(
        ["Paused"],
        ["Continue", "Settings", "Menu", "Exit"],
        ["level:" + level_name, "settings_paused", "start", ExitCodes.STOP]
    ),
}
# fmt: on


def main(screen: curses.window) -> NoReturn:
    """Main curses function"""
    curses.curs_set(False)
    os.environ.setdefault("ESCDELAY", "25")

    window_manager = WindowManager()
    input_getter = InputGetter(screen)
    menu_drawer = MenuLoop(screen, window_manager, input_getter)
    loop = GameLoop(screen, window_manager, input_getter)

    menu = "start"
    while True:
        menu_return = menu_drawer.show_menu(menus[menu])
        if menu_return == ExitCodes.STOP:  # exit via keyboard
            break
        menu = menu_drawer.menu.options_actions[menu_return]
        if menu == ExitCodes.STOP:  # exit via option action choice
            break
        menu_drawer.selected_index = 0

        if menu.startswith("level:"):
            global level_name
            level_name = menu.split(":", 1)[1]
            loop_return = loop.start()
            if loop_return == ExitCodes.STOP:
                break
            elif loop_return == ExitCodes.PAUSE:
                menu = "pause"

    input_getter.quit()


if __name__ == "__main__":
    curses.wrapper(main)
    curses.endwin()
