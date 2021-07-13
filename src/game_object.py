from typing import NoReturn

from datatypes.vector import Vector

# import shape from enums class
# TODO: define shape datatype, orientation datatype, texture datatype


class StaticBody:
    """represents the properties of a shape object"""

    def __init__(self, position: Vector, shape: int, texture: int, orientation: float = 0):
        """Init a new static body object

        Args:
            position (Vector): [description]
            shape ([type]): [description]
            orientation ([type]): [description]
            texture ([type]): [description]
        """
        self.position = position
        self.shape = shape
        self.orientation = orientation
        self.texture = texture

    def get_position(self) -> Vector:
        """Returns position of object"""
        return self.position

    def get_shape(self) -> int:
        """Returns shape of object"""
        return self.shape

    def get_orientation(self) -> float:
        """Returns orientation of object"""
        return self.orientation

    def get_texture(self) -> int:
        """Returns texture of object"""
        return self.texture

    def get_body_parameters(self) -> list[Vector, int, float, int]:
        """Returns body parameters"""
        return [self.position, self.shape, self.orientation, self.texture]

    def set_position(self, position: Vector) -> NoReturn:
        """Sets position of object"""
        self.position = position


class KinematicBody(StaticBody):
    """Represents the physics of a dynamic body"""

    # Physical constants
    MIN_BOUNCE_VELOCITY = 2

    def __init__(
        self,
        position: Vector,
        shape: int,
        texture: int,
        mass: float,
        orientation: float = 0,
        elasticity: float = 0,
        friction: float = 0,
        gravity_magnitude: float = 0,
    ):
        """Init a new dynamic body object

        Args:
            position (Vector): [description]
            shape ([type]): [description]
            orientation ([type]): [description]
            texture ([type]): [description]
            mass (float): [description]
            elasticity (float, optional): [description]. Defaults to 0.
            friction (float, optional): [description]. Defaults to 0.
            gravity_magnitude (float, optional): [description]. Defaults to 0.
        """
        super().__init__(position=position, shape=shape, texture=texture, orientation=orientation)
        self.mass = mass
        self.elasticity = elasticity
        self.friction = friction
        self.gravity_magnitude = gravity_magnitude
        self.accel_x: float = 0
        self.accel_y: float = 0

    def accelerate(self, magnitude_x: float, magnitude_y: float) -> NoReturn:
        """Accelerates the dynamic body"""
        self.accel_x += magnitude_x
        self.accel_y += magnitude_y

    def apply_force(self, force_x: float, force_y: float) -> NoReturn:
        """Apply a force to the dynamic body"""
        self.accel_x += force_x * self.mass
        self.accel_y += force_y * self.mass

    def apply_gravity(self) -> NoReturn:
        """Apply gravity to the dynamic body"""
        self.accelerate(0, self.gravity_magnitude)

    def apply_friction_x(self, x_velo: float, prev_x: float, temp_friction_x: float) -> NoReturn:
        """Not done yet"""
        # TODO: implement friction formulas: Friction(max) = normal reaction * friction coefficient and logic
        # governing friction inheritance
        pass

    def apply_friction_y(self, y_velo: float, prev_y: float, temp_friction_y: float) -> NoReturn:
        """Not done yet"""
        # TODO: implement friction formulas: Friction(max) = normal reaction * friction coefficient and logic
        # governing friction inheritance
        pass

    def get_x_force(self) -> float:
        """Get the force on the x axis"""
        return self.accel_x * self.mass

    def get_y_force(self) -> float:
        """Get the force on the y axis"""
        return self.accel_y * self.mass

    def update(self, *args) -> NoReturn:
        """Not done yet"""
        # TODO: logic to update objects acceleration and velocities
        pass
