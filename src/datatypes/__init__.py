from collections import namedtuple

# Position = namedtuple("Position", ["x", "y"])
# Size = namedtuple("Size", ["width", "height"])
# Rectangle = namedtuple("Rectangle", ["x1", "y1", "x2", "y2"])
# Edges = namedtuple("Corners", ["left", "top", "right", "bottom"])
# Color = namedtuple("Color", ["fg", "bg"])
Menu = namedtuple("Menu", ["text_lines", "options", "options_actions"])

from .game_object import GameObject  # noqa: F401 E402
from .textures import EmptyTexture as EmptyTexture  # noqa: F401 E402
from .textures import Texture as Texture  # noqa: F401 E402
from .vector import Vector as Vector  # noqa: F401 E402
