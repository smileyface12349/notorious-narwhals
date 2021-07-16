import math
import typing
from typing import List, NoReturn, Optional, Tuple, Union

from datatypes.shape import Shape

from .textures import EmptyTexture, Texture
from .vector import Vector

if typing.TYPE_CHECKING:
    from .triggers import Triggers


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
        gravity: Vector = Vector(0, -0.49),
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
        self.static = static
        self.shape = shape
        self.size = size
        self.orientation = orientation
        self.texture = texture
        self.elasticity = elasticity
        self.friction = friction
        self.mass = mass
        self.velocity = velocity
        self.collision = collision
        self.triggers = triggers
        self.forces = forces
        self.z = z
        self.gravity = gravity

        # These attributes are all updated every tick
        self._forces = initial_forces
        self._resultant: Vector = Vector(0, 0)
        self._acceleration: Vector = Vector(0, 0)
        self._touching = []

    def update(self, touching: List[Tuple[float, float, Union["GameObject", int]]] = None) -> NoReturn:
        """Updates the state of the object. Should be called every tick

        :param touching: A list of objects that are in contact with this object, and the angle they are from the
        current object. In the format [min_angle, max_angle, object]. Used to detect collisions
        To signify the edge of the window, 0 should be put in place of the object
        :return:
        """
        if touching is None:
            touching = []

        self._touching = touching

        self.calculate_forces()
        self.calculate_acceleration()

        self.velocity += self._acceleration
        self.position += self.velocity

    def calculate_forces(self) -> List[Vector]:
        """Gets a full list of forces acting on the object during this tick"""
        self._forces = self.forces

        weight = self.mass * self.gravity
        self.add_temp_force(weight)

        self.process_collisions()  # includes any object interactions such as normal reaction forces and friction

        return self._forces

    def process_collisions(self) -> NoReturn:
        """Handles the object colliding with any other objects"""
        resultant: Vector = sum(self._forces)
        direction = self.velocity.direction

        # This assumes that the resultant force is normal to the plane (which it often isn't)
        if resultant.x >= 0:
            plane_normal = 180 - direction
        else:
            plane_normal = direction - 180

        obj = self.get_collision_object(direction=direction)
        if isinstance(obj, int):
            obj = GameObject(static=True, collision=[0])  # edge of the screen
        if obj is not None:
            if obj.static:  # apply a normal reaction force
                reaction = -resultant
                movement_force = -resultant

                # Resolve into two separate forces
                angle_to_normal = (direction - plane_normal) % 90
                reaction *= math.cos(math.radians(angle_to_normal))
                movement_force *= math.sin(math.radians(angle_to_normal))

                self.add_temp_force(reaction)  # this negates the resultant force
                self.add_temp_force(-self.velocity * self.mass)  # this will decelerate the object to 0
                self.process_friction(obj=obj, reaction=reaction, force=movement_force)
            else:  # move the object
                v_1, v_2 = self.calculate_velocity_after_collision(obj=obj)
                self.velocity = v_1
                obj.velocity = v_2

    def process_friction(self, obj: "GameObject", reaction: Vector, force: Vector = Vector(0, 0)) -> NoReturn:
        """Handles the object moving perpendicular to surfaces"""
        coeff: float = self.friction * obj.friction
        f_max: Vector = coeff * reaction

        if f_max > force:  # comparing magnitudes is enough here
            self.add_temp_force(-force)  # just have to entirely oppose the motion
        else:
            self.add_temp_force(f_max)  # add the maximum amount of friction

    def calculate_velocity_after_collision(self, obj: "GameObject") -> Tuple[Vector, Vector]:
        """Calculates the velocity of each object after they collide

        Uses conservation of momentum and conservation of kinetic energy

        This formula isn't particularly elegant, but it seems to work (I derived it)
         - TODO: This has been tested with one test case in one dimension. Most definitely needs more testing
        """
        m_1 = self.mass
        m_2 = obj.mass
        v_1 = self.velocity
        v_2 = obj.velocity

        momentum: Vector = m_1 * v_1 + m_2 * v_2
        energy: float = 1 / 2 * m_1 * v_1.magnitude ** 2 + 1 / 2 * m_2 * v_2.magnitude ** 2
        energy_after = energy * self.elasticity

        # v_1_after = part1 +/- part2
        part1 = 1 / (m_1 + m_2)
        part2_x = math.sqrt((1 + (m_1 + m_2) ** 2 * (energy_after * m_2 - momentum.x ** 2)) / (m_1 * (m_1 + m_2) ** 3))
        part2_y = math.sqrt((1 + (m_1 + m_2) ** 2 * (energy_after * m_2 - momentum.y ** 2)) / (m_1 * (m_1 + m_2) ** 3))
        part1 = Vector(part1, part1)
        part2 = Vector(part2_x + part2_y)

        plus = part1 + part2
        minus = part1 - part2

        collide = self.get_collision_object(plus.direction)
        if id(collide) == id(obj):  # still facing each other
            v_1_after = minus
        else:
            v_1_after = plus

        v_2_after = (momentum - m_1 * v_1_after) / m_2

        return v_1_after, v_2_after

    def get_collision_object(self, direction: float) -> Optional["GameObject"]:
        """Gets the first object that will collide with the current object given the direction of its velocity"""
        for min_angle, max_angle, obj in self._touching:
            if min_angle > max_angle:
                result = min_angle <= direction <= 360 or 0 <= direction <= max_angle
            else:
                result = min_angle <= direction <= max_angle
            if result and self.shares_collision_group(obj):
                return obj

        # nothing to collide with
        return None

    def shares_collision_group(self, obj: "GameObject") -> bool:
        """Checks if the current object should collide/interact with the given object"""
        for group in self.collision:
            for group2 in obj.collision:
                if group == group2:
                    return True

        return False

    def calculate_acceleration(self) -> Vector:
        """Calculates the acceleration. Forces should already be calculated"""
        self._resultant = sum(self._forces)
        self._acceleration = self._resultant / self.mass
        return self._acceleration

    def add_force(self, force: Vector) -> NoReturn:
        """Adds a static force to the object. Stays forever"""
        self.forces.append(force)

    def add_temp_force(self, force: Vector) -> NoReturn:
        """Adds a force to the object, but only for a single tick"""
        self._forces.append(force)

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
