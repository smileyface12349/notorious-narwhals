import operator
import platform
from abc import ABC, abstractmethod
from os import get_terminal_size
from typing import NoReturn, Optional

from datatypes import Edges, Position, Rectangle, Size

current_platform = platform.system()

if current_platform == "Windows":
    import win32console
    import win32gui
elif current_platform == "Linux":
    from Xlib import X
    from Xlib.display import Display
    from Xlib.xobject.drawable import Window
elif current_platform == "Darwin":
    import applescript
else:
    raise RuntimeError("OS is not supported")


class Singleton(type):
    """Metaclass to convert any class into a singleton"""

    def __init__(cls, name, bases, d):  # noqa: ANN001 D101
        super(Singleton, cls).__init__(name, bases, d)
        cls.instance = None

    def __call__(cls, *args, **kwargs):  # noqa: D101 D102
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class ABCSingleton(type(ABC), type(Singleton)):
    """Metaclass that combines ABC and Singleton behavior"""

    pass


class AbstractWindowManager(metaclass=ABCSingleton):
    """Class to get and manage window position and size, as well as movement and resizing"""

    def __init__(self):
        # Window constraints attributes.
        # Set any of them to enable constraints (to disallow resizing or moving the window past a certain point)
        # Set any of them to None to disable constraints
        self.min_size: Optional[Size] = None
        self.max_size: Optional[Size] = None
        self.min_pos: Optional[Position] = None
        self.max_pos: Optional[Position] = None

        self.current_rect: Rectangle = None  # window rect coordinates on current frame
        self.previous_rect: Rectangle = None  # window rectangle coordinates on previous frame

    @staticmethod
    def get_position(rect: Rectangle) -> Position:
        """Extracts position (x, y) from rectangle coordinates (upper left corner)"""
        x1, y1, _, _ = rect
        return Position(x1, y1)

    @staticmethod
    def get_size(rect: Rectangle) -> Size:
        """Extracts size (width, height) from rectangle coordinates"""
        x1, y1, x2, y2 = rect
        width = x2 - x1
        height = y2 - y1
        return Size(width, height)

    def get_font_size(self, rect: Rectangle) -> Size:
        """Extracts size (width, height) of each character as pixels"""
        width = int(self.get_size(rect).width / get_terminal_size().columns)
        height = int(self.get_size(rect).height / get_terminal_size().lines)
        return Size(width, height)

    @property
    def position(self) -> Position:
        """Position (x, y) of the window on current frame (upper left corner)"""
        return self.get_position(self.current_rect)

    @property
    def size(self) -> Size:
        """Size (width, height) of the window on current frame"""
        return self.get_size(self.current_rect)

    @property
    def font_size(self) -> Size:
        """Size (width, height) of each character as pixels"""
        return self.get_font_size(self.current_rect)

    @property
    def rect_diff(self) -> Rectangle:
        """
        Difference between current and previous rectangle coordinates of the window.

        Use translated_edges_by for clearer attributes.
        """
        return Rectangle(*map(operator.sub, self.current_rect, self.previous_rect))

    @property
    def translated_edges_by(self) -> Edges:
        """Same as rect_diff, but with clearer attributes in namedtuple"""
        return Edges(*self.rect_diff)

    @property
    def translated_by(self) -> Position:
        """Difference between current and previous position of the window (upper left corner)"""
        return self.get_position(self.rect_diff)

    @property
    def scaled_by(self) -> Size:
        """Difference between current and previous size of the window (in pixels)"""
        return self.get_size(self.rect_diff)

    @property
    def scaled_by_relative(self) -> Size:
        """Difference between current and previous size of the window (as ratios)"""
        width_current, height_current = self.get_size(self.current_rect)
        width_previous, height_previous = self.get_size(self.previous_rect)

        return Size(width_current / width_previous, height_current / height_previous)

    @property
    def was_moved(self) -> bool:
        """Whether the window was moved relative to previous frame"""
        return self.translated_by != (0, 0)

    @property
    def was_resized(self) -> bool:
        """Whether the window was resized relative to previous frame"""
        return self.scaled_by != (0, 0)

    @property
    def was_changed(self) -> bool:
        """Whether the window was moved or resized relative to previous frame"""
        return self.was_moved or self.was_resized

    def update(self) -> NoReturn:
        """Updates

        Updates current_rect and previous_rect attributes (!)
        Updates window size/position if user changed it past specified constrains

        This method should be called on every frame, and called only once
        This method should be called BEFORE any operations on the window in any given frame,
        including getting values from properties
        """
        self.previous_rect = self.current_rect
        self.current_rect = self._get_window_rect()

        # Resize window to fit constraints
        constrained_rect = self._fit_constraints(self.current_rect)
        if self.current_rect != constrained_rect:
            self._set_window_rect(constrained_rect)
            self.current_rect = constrained_rect

    def _fit_constraints(self, rect: Rectangle) -> Rectangle:
        size = self.get_size(rect)
        if self.min_size and any(map(operator.lt, size, self.min_size)):
            size = tuple(map(max, size, self.min_size))
        if self.max_size and any(map(operator.gt, size, self.max_size)):
            size = tuple(map(min, size, self.max_size))

        pos = self.get_position(rect)
        if self.min_pos and any(map(operator.lt, pos, self.min_pos)):
            pos = tuple(map(max, pos, self.min_pos))
        if self.max_pos and any(map(operator.gt, pos, self.max_pos)):
            pos = tuple(map(min, pos, self.max_pos))

        return Rectangle(*pos, *map(operator.add, pos, size))

    def set_window_rect(self, rect: Rectangle) -> NoReturn:
        """Sets window rectangle coordinates

        Sets window rectangle coordinates to passed rect, adhering to specified in attributes constraints
        For clarity it's better if this method is called no more than once per frame, after everything else
        """
        constrained_rect = self._fit_constraints(rect)
        self._set_window_rect(constrained_rect)
        self.current_rect = constrained_rect

    @abstractmethod
    def _get_window_rect(self) -> Rectangle:
        """Get window position and size as coordinates

        OS - specific implementation of calls
        """
        ...

    @abstractmethod
    def _set_window_rect(self, rect: Rectangle) -> NoReturn:
        """Set window position and size to coordinates

        OS - specific implementation of calls
        """
        ...


class Win32WindowManager(AbstractWindowManager):
    """Window manager class for Win32"""

    def __init__(self):
        super().__init__()
        self.hwnd = win32console.GetConsoleWindow()

    def _get_window_rect(self) -> Rectangle:
        rect = win32gui.GetWindowRect(self.hwnd)
        return Rectangle(*rect)

    def _set_window_rect(self, rect: Rectangle) -> NoReturn:
        hwnd = win32console.GetConsoleWindow()
        win32gui.MoveWindow(hwnd, *self.get_position(rect), *self.get_size(rect), True)


class DarwinWindowManager(AbstractWindowManager):
    """Window manager class for Darwin"""

    def _get_window_rect(self) -> Rectangle:
        rect = applescript.run('tell application "Terminal" to get the bounds of the front window').out.split(", ")
        rect_int = map(int, rect)
        return Rectangle(*rect_int)

    def _set_window_rect(self, rect: Rectangle) -> NoReturn:
        rect_str = ", ".join(map(str, [rect.x1, rect.y1, rect.x2, rect.y2]))
        applescript.run('tell application "Terminal" to set the bounds of the front window to {' + rect_str + "}")


class X11WindowManager(AbstractWindowManager):
    """Window manager class for X11"""

    def __init__(self):
        super().__init__()
        self.display = Display()
        self.root = self.display.screen().root
        self.window_id = self.root.get_full_property(
            self.display.intern_atom("_NET_ACTIVE_WINDOW"), X.AnyPropertyType
        ).value[0]
        self.window = self.display.create_resource_object("window", self.window_id)

    def _get_window_rect(self) -> Rectangle:
        geometry = Window.get_geometry(self.window.query_tree().parent)._data
        rect = (
            geometry.get("x"),
            geometry.get("y"),
            geometry.get("width") + geometry.get("x"),
            geometry.get("height") + geometry.get("y"),
        )
        return Rectangle(*rect)

    def _set_window_rect(self, rect: Rectangle) -> NoReturn:
        self.window.configure(x=rect.x1, y=rect.y1, width=(rect.x2 - rect.x1), height=(rect.y2 - rect.y1))
        self.display.sync()


window_managers = {
    "Windows": Win32WindowManager,
    "Darwin": DarwinWindowManager,
    "Linux": X11WindowManager,
}

WindowManager = window_managers[current_platform]  # import this name to get window manager for current platform!
