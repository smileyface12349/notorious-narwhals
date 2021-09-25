import sys

from .objects.kinematic import FallingObject
from .objects.static import Wall

sys.path.append("..")

from src.box import BoxState  # noqa: E402
from src.datatypes import Vector  # noqa: E402 F401

objects = []

obj = FallingObject(position=Vector(10, 10), collision=[0, 1], z=1, elasticity=0.5, char="O", colour=1)
objects.append(obj)

obj = Wall(position=Vector(0, 11), size=Vector(x=20, y=1), collision=[1], char="_", colour=0)
objects.append(obj)

obj = Wall(position=Vector(relative_x=0.9, relative_y=0.9), size=Vector(relative_x=1, y=1), collision=[1], char="-", colour=0)
objects.append(obj)

level = BoxState(initial_objects=objects)
