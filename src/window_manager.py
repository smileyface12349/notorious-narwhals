import operator
import platform
from abc import ABC, abstractmethod
from typing import Optional

from datatypes import Corners, Position, Rectangle, Size

current_platform = platform.system()

if current_platform == "Windows":
    import win32console
    import win32gui
elif current_platform == "Linux":
    from Xlib.display import Display
    from Xlib.xobject.drawable import Window

    # import linux specific modules
elif current_platform == "Darwin":
    # import linux specific modules
    pass
else:
    raise RuntimeError("OS is not supported")


class AbstractWindowManager(ABC):
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

    @property
    def position(self) -> tuple[int, int]:
        """Position (x, y) of the window on current frame (upper left corner)"""
        return self.get_position(self.current_rect)

    @property
    def size(self) -> tuple[int, int]:
        """Size (width, height) of the window on current frame"""
        return self.get_size(self.current_rect)

    @property
    def rect_diff(self) -> tuple[int, int, int, int]:
        """
        Difference between current and previous rectangle coordinates of the window.
        Use translated_corners_by for clearer attributes
        """
        return Rectangle(*map(operator.sub, self.current_rect, self.previous_rect))

    @property
    def translated_corners_by(self):
        """Same as rect_diff, but with clearer attributes in namedtuple"""
        return Corners(*self.rect_diff)

    @property
    def translated_by(self):
        """Difference between current and previous position of the window (upper left corner)"""
        return self.get_position(self.rect_diff)

    @property
    def scaled_by(self):
        """Difference between current and previous size of the window (in pixels)"""
        return self.get_size(self.rect_diff)

    @property
    def scaled_by_relative(self) -> Size[float, float]:
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
    def changed(self) -> bool:
        """Whether the window was moved or resized relative to previous frame"""
        return self.was_moved or self.was_resized

    def update(self):
        """
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
            self.set_window_rect(constrained_rect)

    def _fit_constraints(self, rect):
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

    def set_window_rect(self, rect: Rectangle):
        """
        Sets window rectangle coordinates to passed rect, adhering to specified in attributes constraints
        For clarity it's better if this method is called no more than once per frame, after everything else
        """
        constrained_rect = self._fit_constraints(rect)
        self._set_window_rect(constrained_rect)
        self.current_rect = constrained_rect

    @abstractmethod
    def _get_window_rect(self) -> Rectangle:
        """
        OS - specific implementation of calls
        to get window position and size to specific coordinates
        """

        ...

    @abstractmethod
    def _set_window_rect(self, rect: Rectangle):
        """
        OS - specific implementation of calls
        to set window position and size to specific coordinates
        """
        ...

    # @abstractmethod
    # def maximize_window(self):
    #     ...


class Win32WindowManager(AbstractWindowManager):
    def __init__(self):
        super().__init__()
        self.hwnd = win32console.GetConsoleWindow()

    def _get_window_rect(self) -> Rectangle:
        rect = win32gui.GetWindowRect(self.hwnd)
        return Rectangle(*rect)

    def _set_window_rect(self, rect: Rectangle):
        hwnd = win32console.GetConsoleWindow()
        win32gui.MoveWindow(hwnd, *self.get_position(rect), *self.get_size(rect), True)


class X11WindowManager(AbstractWindowManager):
    def __init__(self):
        super().__init__()
        self.display = Display()
        self.root = self.display.screen().root
        self.NET_ACTIVE_WINDOW = self.display.intern_atom("_NET_ACTIVE_WINDOW")
        self.active = self.display.get_input_focus().focus
        self.window = []
        while self.active.id != self.root.id:
            self.active = self.active.query_tree().parent
            self.window.append(self.active)

    def _get_window_rect(self):
        geometry = Window.get_geometry(self.window[1])._data
        rect = (
            geometry.get("x"),
            geometry.get("y"),
            geometry.get("width") + geometry.get("x"),
            geometry.get("height") + geometry.get("y"),
        )
        return Rectangle(*rect)

    def _set_window_rect(self, rect: Rectangle):
        pass


window_managers = {
    "Windows": Win32WindowManager,
    "Linux": X11WindowManager,
}

WindowManager = window_managers[current_platform]  # import this name to get window manager for current platform!
