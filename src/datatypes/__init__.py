from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
Size = namedtuple("Size", ["width", "height"])
Rectangle = namedtuple("Rectangle", ["x1", "y1", "x2", "y2"])
Edges = namedtuple("Corners", ["left", "top", "right", "bottom"])
Color = namedtuple("Color", ["fg", "bg"])
Menu = namedtuple("Menu", ["text_lines", "options"])

from .textures import EmptyTexture as EmptyTextureImported  # noqa: E402
from .textures import Texture as TextureImported  # noqa: E402
from .vector import Vector as VectorImported  # noqa: E402

Vector = VectorImported
Texture = TextureImported
EmptyTexture = EmptyTextureImported
