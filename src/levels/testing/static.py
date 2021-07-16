from ...box import BoxState
from ...datatypes import Vector
from ..objects.static import Wall

objects = [Wall(position=Vector(3, 3), size=Vector(5, 5)), Wall(position=Vector(15, 10), size=Vector(2, 30))]

level = BoxState(initial_objects=objects)
