from collections import namedtuple

from .vector import Vector  # noqa: F401

Position = namedtuple("Position", ["x", "y"])
Size = namedtuple("Size", ["width", "height"])
Rectangle = namedtuple("Rectangle", ["x1", "y1", "x2", "y2"])
Corners = namedtuple("Corners", ["top", "bottom", "left", "right"])
Color = namedtuple("Color", ["fg", "bg"])
