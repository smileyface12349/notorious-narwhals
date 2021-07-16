from src.box import BoxState
from src.datatypes import Vector
from src.datatypes.textures import SolidTexture

from ..objects.static import Wall

objects = []

wall1 = Wall(position=Vector(3, 3), size=Vector(5, 5))
wall1.texture = SolidTexture(char="@", colour=69, obj=wall1)
objects.append(wall1)

wall2 = Wall(position=Vector(15, 10), size=Vector(2, 30))
wall2.texture = SolidTexture(char="#", colour=243, obj=wall2)
objects.append(wall2)

level = BoxState(initial_objects=objects)
