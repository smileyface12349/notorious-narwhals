import sys

# Import objects you need
# E.g.: from .objects.static import Wall
# Remove these comments

sys.path.append("..")

from src.box import BoxState  # noqa: E402
from src.datatypes import Vector  # noqa: E402 F401
from src.datatypes.textures import SolidTexture  # noqa: E402 F401

objects = []

# Create you level by appending objects to the objects list
# E.g.: wall = Wall(position=Vector(3, 3), size=Vector(5, 5))
#       wall.texture = SolidTexture(char="@", colour=69, obj=wall1)
#       objects.append(wall)
# Remove these comments

level = BoxState(initial_objects=objects)
