import sys

from .objects.static import Wall

sys.path.append("..")

from src.box import BoxState  # noqa: E402
from src.datatypes import Vector  # noqa: E402

objects = []

wall1 = Wall(position=Vector(3, 3), size=Vector(5, 5), char="@", colour=69)
objects.append(wall1)

wall2 = Wall(position=Vector(15, 10), size=Vector(2, 30), char="#", colour=243)
objects.append(wall2)

level = BoxState(initial_objects=objects)
