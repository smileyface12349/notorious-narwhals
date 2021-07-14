import sys
from typing import List, NoReturn, Tuple, Union

sys.path.append("..")

from src.box import GameObject  # noqa: E402
from src.datatypes import Vector  # noqa: E402


class Texture:
    """Base class for which all textures should inherit from

    When using a texture, you may interact with this class
    When defining a texture, you must choose one of the classes that inherit from this class

    This can be attached to a single object so it updates dynamically with that object
    """

    def __init__(self, obj: GameObject = None):
        """Initialize a Texture

        :param obj: The object this texture belongs to.
        """
        self.object = obj
        self.buffer = []  # buffer of tiles to be rendered, refreshed each frame

    def render(self, position: Vector = None, size: Vector = None, orientation: float = None) -> list:
        """Outputs the texture in a format ready to render

        Takes into account the position, size and orientation of the object

        Output format is [[position: Vector, char: str, colour: int]]
        """
        self.buffer = []

        if not size:
            size = self.object.size
        if not orientation:
            orientation = self.object.orientation
        if not position:
            position = self.object.position

        self.specific_render(position, size, orientation)

        return self.buffer

    def specific_render(self, position: Vector, size: Vector, orientation: float) -> NoReturn:
        """Render method specific to a type of texture

        Populates self.buffer by calling self._buffer_tile()

        This must be overwritten in every subclass
        """
        pass

    def _buffer_tile(self, position: Vector, character: str, colour: int) -> NoReturn:
        """Adds a tile to be rendered in the current buffer"""
        self.buffer.append([position, character, colour])


class SolidTexture(Texture):
    """Represents a texture that is made up of a single character and colour

    Supports variable size and rotations
    """

    def __init__(self, char: str, colour: int, obj: GameObject = None):
        """Initialize a solid texture

        :param char: Single character to span the entire texture
        :param colour: Colour of the texture
        """
        super().__init__(obj=obj)

        self.char = char
        self.colour = colour

    def specific_render(self, position: Vector, size: Vector, orientation: float) -> NoReturn:
        """Render a solid texture"""
        for x in range(round(size.x)):
            for y in range(round(size.y)):
                draw_pos = Vector(round(position.x + x), round(position.y + y))
                self._buffer_tile(draw_pos, self.char, self.colour)


class EmptyTexture(SolidTexture):
    """An entirely transparent texture, mostly used internally when textures are not specified"""

    def __init__(self, obj: GameObject = None):
        super().__init__(obj=obj, char="TRANSPARENT", colour=0)


class FixedTexture(Texture):
    """Represents a texture that cannot change size or orientation

    This allows every tile to be defined
    """

    def __init__(self, texture: List[List[str, int]], obj: GameObject = None):
        """Initialize a fixed texture

        Texture will seamlessly wrap around lines as defined by the size of the object. Do not implement line breaks
        Total length of the texture must be equal to the (fixed) area of the object

        :param texture: A list of elements in the form [text, colour] going from left to right, top to bottom
        """
        super().__init__(obj=obj)
        self.texture = texture

    def specific_render(self, position: Vector, size: Vector, orientation: float) -> NoReturn:
        """Renders the fixed texture"""
        chars = self.next_character()
        for x in range(round(size.x)):  # x is first because co-ordinates are given as y, x
            for y in range(round(size.y)):
                try:
                    next_char = next(chars)
                except StopIteration:
                    empty = EmptyTexture()
                    next_char = (empty.char, empty.colour)
                self._buffer_tile(Vector(round(x + position.x), round(y + position.y)), next_char[0], next_char[1])

    def next_character(self) -> Tuple[str, int]:
        """Iterate over all characters in the texture"""
        for text, colour in self.texture:
            for char in text:
                yield char, colour


class RotatingTexture(Texture):
    """Represents a texture that cannot change size, but can rotate

    This allows every tile to be defined
    """

    def __init__(self, texture: Union[List[List[float, float, Texture]], List[List[Texture]]], obj: GameObject = None):
        """
        Angles are measured clockwise from directly upwards in degrees

        If min_angle is greater than max_angle, the range will still work and always go clockwise (e.g. 315 to 45)
        If none match, the last element of the list is used.

        It is suggested to use at least 8 points of rotation. If customising individual pixels is not required,
        either VariableTexture or SolidTexture could be more appropriate

        :param texture: A list of elements in the form [min_angle, max_angle, Texture], optionally containing a
        default case at the end of simply [Texture]
        """
        super().__init__(obj=obj)

        self.texture = texture

    def specific_render(self, position: Vector, size: Vector, orientation: float) -> NoReturn:
        """Renders a rotating texture"""
        texture = self.choose_texture(orientation)
        return texture.specific_render(position, size, orientation)

    def choose_texture(self, orientation: float) -> Texture:
        """Chooses the first valid texture that matches the orientation"""
        for texture in self.texture:
            if len(texture) == 1:  # match any
                return texture[0]
            else:
                min_angle, max_angle, texture = texture
                if min_angle > max_angle:
                    result = min_angle <= orientation <= 360 or 0 <= orientation <= max_angle
                else:
                    result = min_angle <= orientation <= max_angle
                if result:
                    return texture[0]

        # none have matched
        return EmptyTexture(obj=self.object)


class VariableTexture(Texture):
    """Represents a texture that can change size and orientation

    Without nesting textures, only certain tiles can be defined. By nesting many texture objects,
    per-tile configuration is possible but difficult. When the remaining area becomes zero, the middle is simply
    ignored
    """

    def __init__(
        self,
        middle: Union["VariableTexture", "SolidTexture"],
        edge: "SolidTexture",
        specific_edges: list = None,
        obj: GameObject = None,
    ):
        """Initialize a variable texture

        :param middle: The texture to fill the middle. Texture must be resizable
        :param edge: A single-character texture to fill in all edge tiles. Overwritten by 'specific_edges'
        :param specific_edges: Customise specific edges / corners. Can define relative to original object
        or rotated object  [TODO]
        """
        super().__init__(obj=obj)

    def specific_render(self, position: Vector, size: Vector, orientation: float) -> NoReturn:
        """Render a variable texture"""
        # TODO


class CompositeTexture(Texture):
    """Divide a texture into two, rendering each separately

    Can split either horizontally or vertically
    """

    def __init__(
        self,
        texture1: Texture,
        texture2: Texture,
        split_value: Union[float, int],
        vertically: bool = False,
        obj: GameObject = None,
    ):
        """
        All values are based on the object as if it was not rotated

        :param texture1: First texture (left or top)
        :param texture2: Second texture (right or bottom)
        :param split_value: The x or y value at which to split on. If this is between 0 and 1, splits at that
        proportion of the size. If it is greater than 1, splits at an absolute coordinate
        :param vertically: Whether to split horizontally or vertically
        """
        super().__init__(obj=obj)

        self.texture1 = texture1
        self.texture1.object = self.object
        self.texture2 = texture2
        self.texture2.object = self.object

        self.split_value = split_value
        self.vertically = vertically

    def specific_render(self, position: Vector, size: Vector, orientation: float) -> NoReturn:
        """Renders a composite texture"""
        if self.split_value >= 1:
            split_coord = self.split_value
        else:
            if self.vertically:
                split_coord = round(self.split_value * size.y)
            else:
                split_coord = round(self.split_value * size.x)

        size1 = size.copy()
        pos1 = position.copy()
        size2 = size.copy()
        pos2 = position.copy()

        if self.vertically:
            size1.y = split_coord
            size2.y = split_coord
            pos2.y = split_coord
        else:
            size1.x = split_coord
            size1.x = split_coord
            pos2.x = split_coord

        self.texture1.specific_render(pos1, size1, orientation)
        self.texture2.specific_render(pos2, size2, orientation)
