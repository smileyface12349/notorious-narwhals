from typing import NoReturn

from datatypes import Vector

# import shape from enums class
# TODO: define shape datatype, orientation datatype, texture datatype


class StaticBody:
    """represents the properties of a shape object"""

    def __init__(self, position: Vector, shape: int, texture: int, size: Vector = (1, 1), orientation: float = 0):
        """Init of a static body object

        Args:
            position (Vector): position of object where units are in tiles
            shape (int): shape type for object, int corresponds to enum for shape
            texture (int): texture type for object, int corresponds to texture type
            size (Vector, optional): Size of object, position corresponds to the upper-left of the object.
            Defaults to (1, 1).
            orientation (float, optional): Clockwise rotation from directly upwards in degrees. Defaults to 0.
        """
        self.position = position
        self.shape = shape
        self.size = size
        self.orientation = orientation
        self.texture = texture

    def get_position(self) -> Vector:
        """Returns position of object"""
        return self.position

    def get_shape(self) -> int:
        """Returns shape of object"""
        return self.shape

    def get_size(self) -> Vector:
        """Returns size of object"""
        return self.size

    def get_orientation(self) -> float:
        """Returns orientation of object"""
        return self.orientation

    def get_texture(self) -> int:
        """Returns texture of object"""
        return self.texture

    def get_body_parameters(self) -> "list[Vector, int, float, int]":
        """Returns body parameters"""
        return [self.position, self.shape, self.orientation, self.texture]

    def set_position(self, position: Vector) -> NoReturn:
        """Sets position of object"""
        self.position = position

    def set_size(self, size: Vector) -> NoReturn:
        """Sets size of object"""
        self.size = size


class KinematicBody(StaticBody):
    """Represents the physics of a dynamic body"""

    def __init__(
        self,
        position: Vector,
        shape: int,
        texture: int,
        mass: float,
        z: int = 0,
        collision: int = 1,
        orientation: float = 0,
        elasticity: float = 0,
        friction: float = 0,
        velocity: Vector = (0, 0),
        gravity: Vector = (0, -0.49),
        size: Vector = (1, 1),
        forces: list = [],
        # triggers: 'list[float, float, float, int]' = [],
    ):
        """[summary]

        Args:
            position (Vector): position of object where units are in tiles
            shape (int): shape type for object, int corresponds to enum for shape
            texture (int): texture type for object, int corresponds to texture type
            mass (float): in kg, determines the amount of exerted force
            z (int, optional): Determines which object is displayed on top. Defaults to 0.
            collision (int, optional):
            orientation (float, optional): Clockwise rotation from directly upwards in degrees. Defaults to 0.
            elasticity (float, optional): The bouncyness of an object, value determines the
            proportion of kinetic energy conserved. Defaults to 0.
            friction (float, optional): Friction coeff. Defaults to 0.
            z (int, optional): Determines which object is displayed on top. Defaults to 0.
            velocity (Vector, optional): How fast an object is moving. Defaults to (0, 0).
            gravity (Vector, optional): Acceleration of freefall. Defaults to (0, -0.49).
            size (Vector, optional): Size of object, Defaults to to (1,1).
            forces (list, optional): list of external forces that object has. Defaults to [].


        """
        super().__init__(position=position, shape=shape, texture=texture, orientation=orientation, size=size)
        self.mass = mass
        self.z = z
        self.elasticity = elasticity
        self.friction = friction
        self.velocity = velocity
        self.gravity = gravity
        self.forces = forces
        # self.triggers = triggers
        self.collision = collision

    def get_mass(self) -> float:
        """Returns mass of object"""
        return self.mass

    def get_z(self) -> int:
        """Returns z of object"""
        return self.z

    def get_elasticity(self) -> float:
        """Returns elasticity of object"""
        return self.elasticity

    def get_friction(self) -> float:
        """Returns friction of object"""
        return self.friction

    def get_velocity(self) -> Vector:
        """Returns velocity of object"""
        return self.velocity

    def get_gravity(self) -> Vector:
        """Returns gravity of object"""
        return self.gravity

    def get_forces(self) -> Vector:
        """Returns forces of object"""
        return self.forces

    # def get_triggers(self) -> list:
    #     """Returns triggers of object"""
    #     return self.triggers

    def get_collision(self) -> int:
        """Returns collision group of object"""
        return self.collision

    def get_velocity_magnitude(self) -> int:
        """Returns velocity magnitude of object"""
        return Vector.magnitude(self.velocity)

    def get_momentum(self) -> float:
        """Returns the momentum of object"""
        return Vector.magnitude(self.velocity) * self.mass

    def set_z(self, z: int) -> NoReturn:
        """Sets value of z of object"""
        self.z = z

    def set_velocity(self, velocity: Vector) -> NoReturn:
        """Sets velocity of object"""
        self.velocity = velocity

    def set_forces(self, forces: list) -> NoReturn:
        """Sets value of forces object"""
        self.forces = forces

    def process_trigger(self, trigger: list) -> NoReturn:
        """Sets value of processes triggers for object"""
        if trigger is not None:
            pass
