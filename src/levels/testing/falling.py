import sys

from ..objects.kinematic import FallingObject
from ..objects.static import Wall

sys.path.append("..")

from src.box import BoxState  # noqa: E402
from src.datatypes import Vector  # noqa: E402 F401
from src.datatypes.textures import SolidTexture  # noqa: E402 F401

objects = []

obj = FallingObject(position=Vector(relative_x=0.5, relative_y=0.5), collision=[1])
obj.texture = SolidTexture(char="O", colour=1, obj=obj)
objects.append(obj)

obj = Wall(position=Vector(relative_x=0.4, relative_y=0.8), size=Vector(relative_x=0.2, y=1), collision=[1], z=1)
obj.texture = SolidTexture(char="_", colour=0, obj=obj)
objects.append(obj)

level = BoxState(initial_objects=objects)
