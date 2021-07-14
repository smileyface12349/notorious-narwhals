from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
Size = namedtuple("Size", ["width", "height"])
Rectangle = namedtuple("Rectangle", ["x1", "y1", "x2", "y2"])
Edges = namedtuple("Corners", ["left", "top", "right", "bottom"])
Color = namedtuple("Color", ["fg", "bg"])
Menu = namedtuple("Menu", ["text_lines", "options"])

from .vector import Vector as VectorImported  # noqa: E402

Vector = VectorImported
