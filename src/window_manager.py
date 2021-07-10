import operator
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Optional

Position = namedtuple("Position", ["x", "y"])
Size = namedtuple("Size", ["width", "height"])
Rectangle = namedtuple("Rectangle", ["x1", "y1", "x2", "y2"])
Corners = namedtuple("Corners", ["top", "bottom", "left", "right"])


class WindowManager(ABC):
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
        height = y2 - x1
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

    def _check_constraints(self):
        pass
        # size_changed = False
        # size = tuple(self.size)
        #
        # if self.min_size and any(map(operator.lt, size, self.min_size)):
        #     size_changed = True
        #     size = tuple(map(max, size, self.min_size))
        #
        # if self.max_size and any(map(operator.gt, size, self.max_size)):
        #     size_changed = True
        #     size = tuple(map(min, size, self.max_size))
        #
        # pos_changed = False
        # pos = tuple(self.position)
        #
        # if self.min_pos and any(map(operator.lt, pos, self.min_pos)):
        #     pos_changed = True
        #     size = tuple(map(max, pos, self.min_pos))
        #
        # if self.max_pos and any(map(operator.gt, pos, self.max_pos)):
        #     pos_changed = True
        #     size = tuple(map(min, pos, self.max_pos))

        # TODO

        # if size_changed or pos_changed:
        #     pass

    def set_window_rect(self, rect: Rectangle):
        """
        Sets window rectangle coordinates to passed rect, adhering to specified in attributes constrains
        For clarity it's better if this method is called no more than once per frame, after everything else
        """
        # todo _check_constraints
        self._set_window_rect(rect)
        self.current_rect = rect

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
