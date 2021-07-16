import sys

from ..objects.static import GameZone, Wall

objects = []


# Level Play area
game_zone = GameZone(50)

objects.append(game_zone.wall_top)
objects.append(game_zone.wall_bottom)
objects.append(game_zone.wall_right)
objects.append(game_zone.wall_left)


wall3 = Wall(
    position=Vector(3, 10),
    size=Vector(4, 4),
    velocity=Vector(100, 100),
    orientation=5,
    mass=10,
    initial_forces=[Vector(100, 100)],
    gravity=Vector(1, -0.49),
    forces=[Vector(20, 20)],
    z=1,
)
wall3.texture = SolidTexture(char="#", colour=121, obj=wall3)
objects.append(wall3)

level = BoxState(initial_objects=objects)
