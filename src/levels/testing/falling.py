import sys

sys.path.append("..")

from src.box import BoxState  # noqa: E402
from src.datatypes import GameObject  # noqa: E402
from src.datatypes import Vector  # noqa: E402 F401

objects = []

obj = GameObject(
    position=Vector(relative_x=0.5, relative_y=0.5),
    collision=[1],
    z=1,
    elasticity=0.5,
    char="O",
    colour=1,
    static=False,
)
objects.append(obj)

obj = GameObject(
    position=Vector(relative_x=0.4, relative_y=0.8),
    size=Vector(relative_x=0.2, y=1),
    collision=[1],
    char="_",
    colour=0,
    static=True,
)
objects.append(obj)

level = BoxState(initial_objects=objects)
