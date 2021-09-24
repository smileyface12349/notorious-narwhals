import math
import sys
import typing
from typing import List, NoReturn, Optional, Tuple, Union

import pymunk

sys.path.append("..")

from src.datatypes.shape import Shape  # noqa: E402

from .textures import EmptyTexture, Texture  # noqa: E402
from .vector import Vector  # noqa: E402

if typing.TYPE_CHECKING:
    from .triggers import Triggers  # noqa: E402


class GameObject:
    """Represents a static or kinematic object that exists within the level"""

    def __init__(
        self,
        position: Vector = Vector(0, 0),
        shape: Shape = Shape.Rectangle,
        size: Vector = Vector(1, 1),
        orientation: float = 0,
        texture: Texture = EmptyTexture(),
        elasticity: float = 0,
        friction: float = 0,
        mass: float = 1,
        velocity: Vector = Vector(0, 0),
        forces: List[Vector] = None,
        triggers: "Triggers" = None,
        collision: List[int] = None,
        z: int = 0,
        gravity: Vector = Vector(0, 0.03),
        static: bool = False,
        initial_forces: List[Vector] = None,
    ):
        """Initialize a new game object"""
        # Replacing mutable default arguments
        if collision is None:
            collision = [1]
        if triggers is None:
            triggers = []
        if forces is None:
            forces = []
        if initial_forces is None:
            forces = []

        # These attributes stay the same between game ticks
        self.position = position
        self.shape = shape
        self.size = size
        self.orientation = orientation
        self.elasticity = elasticity
        self.friction = friction
        self.z = z
        self.mass = mass

        self.body = pymunk.Body()
        self.body.position = (self.position.x, self.position.y)

        if self.shape == Shape.Rectangle:
            self.poly = pymunk.Poly.create_box(self.body)
            self.poly.mass = self.mass

    def update(self) -> NoReturn:
        """Updates the state of the object. Should be called every tick"""

    def render(self) -> list:
        """A helper method to render the object"""
        return self.texture.render()

    def __ge__(self, other: "GameObject") -> bool:
        """Compares z value"""
        return self.z >= other.z

    def __gt__(self, other: "GameObject") -> bool:
        """Compares z value"""
        return self.z > other.z

    def __le__(self, other: "GameObject") -> bool:
        """Compares z value"""
        return self.z <= other.z

    def __lt__(self, other: "GameObject") -> bool:
        """Compares z value"""
        return self.z < other.z
