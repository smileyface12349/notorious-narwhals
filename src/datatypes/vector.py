import math
import sys
from typing import Union

sys.path.append("..")

from src.window_manager import WindowManager  # noqa: E402

window_manager = WindowManager()


class Vector:
    """Represents a 2D vector"""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        *,
        relative_x: float = 0,
        relative_y: float = 0,
        ratio_x: float = 0,
        ratio_y: float = 0,
        initial_pos_x: float = None,
        initial_pos_y: float = None,
    ):
        """Initialize a new Vector

        :param x: Constant value in tiles
        :param y: Constant value in tiles
        :param relative_x: The proportion of the width of the window to add on. Can be negative
        :param relative_y: The proportion of the height of the window to add on. Can be negative
        :param ratio_x: The proportion of how far the window has moved from its original position to add on
        :param ratio_y: The proportion of how far the window has moved from its original position to add on
        :param initial_pos_x: The horizontal position of the window at the start of the level. If unspecified,
        uses the position when the Vector object is initialized
        :param initial_pos_y: The vertical position of the window at the start of the level. If unspecified,
        uses the position when the Vector object is initialized
        """
        self.constant_x: float = x
        self.constant_y: float = y
        self.relative_x: float = relative_x
        self.relative_y: float = relative_y
        self.ratio_x: float = ratio_x
        self.ratio_y: float = ratio_y

        # to prevent circular imports, these are only calculated when first accessed
        self._default_window_x = initial_pos_x
        self._default_window_y = initial_pos_y

    def copy(self) -> "Vector":
        """Returns an identical copy of the vector, preserving all relative information"""
        return Vector(
            x=self.constant_x,
            y=self.constant_y,
            relative_x=self.relative_x,
            relative_y=self.relative_y,
            ratio_x=self.ratio_x,
            ratio_y=self.ratio_y,
            initial_pos_x=self.default_window_x,
            initial_pos_y=self.default_window_y,
        )

    def fixed_copy(self) -> "Vector":
        """Returns a copy of the vector with all relative attributes becoming constant

        This has the effect of 'pausing' it in place, so it will no longer move with the window
        """
        return Vector(x=self.x, y=self.y)

    def to_pixels(self) -> "Vector":
        """Returns a new Vector with co-ordinates converted from tiles into pixels"""
        new = self.copy()
        new.x = self.to_pixels_x(new.x)
        new.y = self.to_pixels_y(new.y)
        return new

    def to_tiles(self) -> "Vector":
        """Returns a new Vector with co-ordinates converted from pixels into tiles"""
        new = self.copy()
        new.x = self.to_tiles_x(new.x)
        new.y = self.to_tiles_y(new.y)
        return new

    @staticmethod
    def to_pixels_x(value: float) -> float:
        """Converts a horizontal distance from tiles into pixels"""
        return value * window_manager.font_size[0]

    @staticmethod
    def to_pixels_y(value: float) -> float:
        """Converts a vertical distance from tiles into pixels"""
        return value * window_manager.font_size[1]

    @staticmethod
    def to_tiles_x(value: float) -> float:
        """Converts a horizontal distance from pixels into tiles"""
        return value / window_manager.font_size[0]

    @staticmethod
    def to_tiles_y(value: float) -> float:
        """Converts a vertical distance from pixels into tiles"""
        return value / window_manager.font_size[1]

    @property
    def x(self) -> float:
        """Horizontal part of the vector"""
        return (
            self.constant_x
            + self.relative_x * self.window_width
            + self.ratio_x * (self.window_x - self.default_window_x)
        )

    @x.setter
    def x(self, value: float) -> None:
        """Adjusts all values equally to get the desired x value"""
        scalar = value / self.x
        self.constant_x *= scalar
        self.relative_x *= scalar
        self.ratio_x *= scalar

    def update_constant_x(self, value: float) -> None:
        """Adjusts only constant_x to get the desired x value"""
        diff = value - self.x
        self.constant_x += diff

    @property
    def y(self) -> float:
        """Vertical part of the vector"""
        return (
            self.constant_y
            + self.relative_y * self.window_height
            + self.ratio_y * (self.window_y - self.default_window_y)
        )

    @y.setter
    def y(self, value: float) -> None:
        """Adjusts all values equally to get the desired y value"""
        scalar = value / self.y
        self.constant_y *= scalar
        self.relative_y *= scalar
        self.ratio_y *= scalar

    def update_constant_y(self, value: float) -> None:
        """Adjusts only constant_y to get the desired y value"""
        diff = value - self.y
        self.constant_y += diff

    @property
    def magnitude(self) -> float:
        """Gets the magnitude of the vector"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @magnitude.setter
    def magnitude(self, value: float) -> None:
        """Scales the value of x and y while keeping the direction the same"""
        scalar = value / self.magnitude
        self.x *= scalar
        self.y *= scalar

    @property
    def direction(self) -> float:
        """Gets the direction of the vector

        Measured as the clockwise angle from directly upwards in degrees
        Vectors with a magnitude of zero will result in an angle of zero
        """
        if self.x == 0:  # this will lead to a ZeroDivisionError
            if self.y >= 0:  # upwards
                return 0
            else:  # downwards
                return 180
        angle = math.degrees(math.atan(self.y / self.x))  # this gets the angle to the horizontal
        if self.x >= 0:
            return 90 - angle
        else:
            return 270 - angle  # tan is periodic every 180, so we need to add on 180 if x is negative

    @direction.setter
    def direction(self, value: float) -> None:
        """Adjusts the value of x and y while keeping the magnitude the same"""
        self.x = math.sin(math.radians(value)) * self.x
        self.y = math.cos(math.radians(value)) * self.y

    def __add__(self, other: "Vector") -> "Vector":
        """Add together two vectors"""
        new = self.copy()
        new.x += other.x
        new.y += other.y
        return new

    def __sub__(self, other: "Vector") -> "Vector":
        """Subtract two vectors"""
        new = self.copy()
        new.x -= other.x
        new.y -= other.y
        return new

    def __mul__(self, other: float) -> "Vector":
        """Multiply a vector by a scalar"""
        new = self.copy()
        new.x *= other
        new.y *= other
        return new

    def __rmul__(self, other: float) -> "Vector":
        """Multiply a scalar by a vector"""
        new = self.copy()
        new.x *= other
        new.y *= other
        return new

    def __truediv__(self, other: float) -> "Vector":
        """Divide a vector by a scalar"""
        new = self.copy()
        new.x /= other
        new.y /= other
        return new

    def __neg__(self) -> "Vector":
        """Negates the x and y coordinates of the vector (180 degree rotation)"""
        new = self.copy()
        new.x = -new.x
        new.y = -new.y
        return new

    def __ge__(self, other: Union[float, "Vector"]) -> bool:
        """Compares the magnitude of the vector with either another vector or a scalar"""
        if isinstance(other, Vector):
            return self.magnitude >= other.magnitude
        else:
            return self.magnitude >= other

    def __gt__(self, other: Union[float, "Vector"]) -> bool:
        """Compares the magnitude of the vector with either another vector or a scalar"""
        if isinstance(other, Vector):
            return self.magnitude > other.magnitude
        else:
            return self.magnitude > other

    def __le__(self, other: Union[float, "Vector"]) -> bool:
        """Compares the magnitude of the vector with either another vector or a scalar"""
        if isinstance(other, Vector):
            return self.magnitude <= other.magnitude
        else:
            return self.magnitude <= other

    def __lt__(self, other: Union[float, "Vector"]) -> bool:
        """Compares the magnitude of the vector with either another vector or a scalar"""
        if isinstance(other, Vector):
            return self.magnitude < other.magnitude
        else:
            return self.magnitude < other

    def __eq__(self, other: Union[float, "Vector"]) -> bool:
        """Compares the magnitude and direction with another vector, or just magnitude with a scalar"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            return self.magnitude == other

    def __ne__(self, other: Union[float, "Vector"]) -> bool:
        """Compares the magnitude and direction with another vector, or just magnitude with a scalar"""
        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        else:
            return self.magnitude != other

    def __abs__(self) -> "Vector":
        """Make both coordinates positive"""
        new = self.copy()
        new.x = abs(self.x)
        new.y = abs(self.y)
        return new

    def __str__(self) -> str:
        """Outputs a string representation in the form (x, y) to 2 decimal places"""
        return f"({self.x:.2f}, {self.y:.2f})"

    def __float__(self) -> float:
        """Gets the scalar form (magnitude) of the vector"""
        return self.magnitude

    def __complex__(self) -> complex:
        """Convert into a complex number"""
        return complex(self.x, self.y)

    def __bool__(self) -> bool:
        """Considered True if the magnitude is non-zero"""
        return self.magnitude != 0

    @property
    def window_width(self) -> float:
        """Current width of the window"""
        return self.to_tiles_x(window_manager.size[0])

    @property
    def window_height(self) -> float:
        """Current height of the window"""
        return self.to_tiles_y(window_manager.size[1])

    @property
    def window_x(self) -> float:
        """Position of the window on the screen (x coordinate)"""
        return self.to_tiles_x(window_manager.position[0])

    @property
    def window_y(self) -> float:
        """Position of the window on the screen (y coordinate)"""
        return self.to_tiles_y(window_manager.position[1])

    @property
    def default_window_x(self) -> float:
        """Gets the original position of the window"""
        if not self._default_window_x:
            self._default_window_x = self.window_x
        return self._default_window_x

    @property
    def default_window_y(self) -> float:
        """Gets the original position of the window"""
        if not self._default_window_y:
            self._default_window_y = self.window_y
        return self._default_window_y
