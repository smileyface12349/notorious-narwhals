import math

from src.window_manager import WindowManager


class Vector:
    """Represents a value with both direction and magnitude"""

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
        initial_pos_y: float = None
    ):
        """Initialize a new Vector

        :param x: Constant value in tiles
        :param y: Constant value in tiles
        :param relative_x: The proportion of the width of the window to add on. Can be negative
        :param relative_y: The proportion of the height of the window to add on. Can be negative
        :param ratio_x: The proportion of how far the window has moved from its original position to add on
        :param ratio_y: The proportion of how far the window has moved from its original position to add on
        :param initial_pos_x: The position of the window at the start of the level. If unspecified,
        uses the position when the Vector object is initialized
        :param initial_pos_y: The position of the window at the start of the level. If unspecified,
        uses the position when the Vector object is initialized
        """

        self.constant_x: float = x
        self.constant_y: float = y
        self.relative_x: float = relative_x
        self.relative_y: float = relative_y
        self.ratio_x: float = ratio_x
        self.ratio_y: float = ratio_y

        if not initial_pos_x:
            initial_pos_x = self.window_x
        self.default_window_x = initial_pos_x
        if not initial_pos_y:
            initial_pos_y = self.window_y
        self.default_window_y = initial_pos_y

        self.window_manager = WindowManager()

    def copy(self):
        """Returns an identical copy of the vector

        Used in some operations to compare vectors"""
        return Vector(
            x=self.constant_x,
            y=self.constant_y,
            relative_x=self.relative_x,
            relative_y=self.relative_y,
            ratio_x=self.ratio_x,
            ratio_y=self.ratio_y,
        )

    def fixed_copy(self):
        """Returns a copy of the vector with all relative attributes becoming constant

        This has the effect of 'pausing' it in place, so it will no longer move with the window"""
        return Vector(x=self.x, y=self.y)

    @property
    def x(self) -> float:
        return (
            self.constant_x
            + self.relative_x * self.window_width
            + self.ratio_x * (self.window_x - self.default_window_x)
        )

    @x.setter
    def x(self, value):
        """Adjusts all values equally to get the desired x value"""
        scalar = value / self.x
        self.constant_x *= scalar
        self.relative_x *= scalar
        self.ratio_x *= scalar

    def update_constant_x(self, value):
        """Adjusts only constant_x to get the desired x value"""
        diff = value - self.x
        self.constant_x += diff

    @property
    def y(self) -> float:
        return (
            self.constant_y
            + self.relative_y * self.window_height
            + self.ratio_y * (self.window_y - self.default_window_y)
        )

    @y.setter
    def y(self, value):
        scalar = value / self.y
        self.constant_y *= scalar
        self.relative_y *= scalar
        self.ratio_y *= scalar

    def update_constant_y(self, value):
        """Adjusts only constant_y to get the desired x value"""
        diff = value - self.y
        self.constant_y += diff

    @property
    def magnitude(self) -> float:
        """Gets the magnitude of the vector"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @magnitude.setter
    def magnitude(self, value):
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
        angle = math.atan(math.degrees(self.y / self.x))  # this gets the angle to the horizontal
        if self.x >= 0:
            return 90 - angle
        else:
            return 270 - angle  # tan is periodic every 180, so we need to add on 180 if it's on the left

    @direction.setter
    def direction(self, value):
        """Adjusts the value of x and y while keeping the magnitude the same"""
        self.x = math.sin(math.degrees(value)) * self.x
        self.y = math.cos(math.degrees(value)) * self.y

    def __add__(self, other):
        """Other value must be another Vector"""
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        """Other value must be another Vector"""
        self.x -= other.x
        self.y -= other.y

    def __mul__(self, other):
        """Other value must be a scalar"""
        self.x *= other
        self.y *= other

    def __truediv__(self, other):
        """Other value must be a scalar"""
        self.x /= other
        self.y /= other

    def __floordiv__(self, other):
        """Other value must be a scalar"""
        self.x //= other
        self.y //= other

    def __ge__(self, other):
        """Compares magnitude"""
        if isinstance(other, Vector):
            return self.magnitude >= other.magnitude
        else:
            return self.magnitude >= other

    def __gt__(self, other):
        """Compares magnitude"""
        if isinstance(other, Vector):
            return self.magnitude > other.magnitude
        else:
            return self.magnitude > other

    def __le__(self, other):
        """Compares magnitude"""
        if isinstance(other, Vector):
            return self.magnitude <= other.magnitude
        else:
            return self.magnitude <= other

    def __lt__(self, other):
        """Compares magnitude"""
        if isinstance(other, Vector):
            return self.magnitude < other.magnitude
        else:
            return self.magnitude < other

    def __eq__(self, other):
        """Compares magnitude and direction"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            return self.magnitude == other

    def __ne__(self, other):
        """Compares magnitude and direction"""
        if isinstance(other, Vector):
            return self.x != other.x or self.y != other.y
        else:
            return self.magnitude != other

    def __abs__(self):
        """Make both coordinates positive"""
        self.x = abs(self.x)
        self.y = abs(self.y)

    def __str__(self):
        """Outputs a string representation in the form (x, y)"""

    def __float__(self):
        """Gets the scalar form (magnitude) of the vector"""
        return self.magnitude

    def __complex__(self):
        """Convert into a complex number"""
        return complex(self.x, self.y)

    def __bool__(self):
        """Considered True if the magnitude is non-zero"""
        return self.magnitude != 0

    @property
    def window_width(self):
        """Current width of the window"""
        return self.window_manager.size[0]

    @property
    def window_height(self):
        """Current height of the window"""
        return self.window_manager.size[1]

    @property
    def window_x(self):
        """Position of the window on the screen (x coordinate)"""
        return self.window_manager.position[0]

    @property
    def window_y(self):
        """Position of the window on the screen (y coordinate)"""
        return self.window_manager.position[1]
