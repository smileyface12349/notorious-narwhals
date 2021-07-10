from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
Size = namedtuple("Size", ["width", "height"])
Rectangle = namedtuple("Rectangle", ["x1", "y1", "x2", "y2"])
Corners = namedtuple("Corners", ["top", "bottom", "left", "right"])
