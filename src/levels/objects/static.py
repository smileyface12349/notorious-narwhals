import sys

sys.path.append("..")

from src.datatypes import GameObject  # noqa: E402
from src.datatypes import Vector  # noqa: E402
from src.datatypes.textures import SolidTexture  # noqa: E402


class Wall(GameObject):
    """A static object that does not move"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static = True


class GameZone(Wall):
    """Creates the play zone"""

    def __init__(self, box_size: int, wall_thickness: int = 1, square: bool = False, *args, **kwargs):
        """Create a new play zone with Walls"""
        super().__init__(*args, **kwargs)
        # Makes sure play area look like a square where pixel of char is 8x16
        if square is False:
            _square_divider = 1
        else:
            _square_divider = 2

        self.wall_top = Wall(position=Vector(0, 0), size=Vector(box_size, wall_thickness), z=0)
        self.wall_top.texture = SolidTexture(char="-", colour=121, obj=self.wall_top)

        self.wall_bottom = Wall(
            position=Vector(0, box_size / _square_divider + 1), size=Vector(box_size, wall_thickness), z=0
        )
        self.wall_bottom.texture = SolidTexture(char="-", colour=121, obj=self.wall_bottom)

        self.wall_left = Wall(position=Vector(0, 1), size=Vector(wall_thickness, box_size / _square_divider), z=0)
        self.wall_left.texture = SolidTexture(char="|", colour=121, obj=self.wall_left)

        self.wall_right = Wall(
            position=Vector((box_size - wall_thickness), wall_thickness),
            size=Vector(wall_thickness, box_size / _square_divider),
            z=0,
        )
        self.wall_right.texture = SolidTexture(char="|", colour=121, obj=self.wall_right)
