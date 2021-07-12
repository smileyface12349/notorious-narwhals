from datatypes.vector import Vector

# import shape from enums class
# TODO: define shape datatype, orientation datatype, texture datatype


class StaticBody:
    """represents the properties of a shape object"""

    def __init__(self, position: Vector, shape: int, texture: int, orientation: float = 0):
        """Init a new shape object

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

    def get_shape(self):
        """Returns shape of object"""
        return self.shape

    def get_orientation(self):
        """Returns orientation of object"""
        return self.orientation

    def get_texture(self):
        """Returns texture of object"""
        return self.texture

    def get_body_parameters(self):
        """Returns body parameters"""
        return [self.position, self.shape, self.orientation, self.texture]

    def set_position(self, position: Vector) -> Vector:
        """Sets position of object"""
        self.position = position


class KinematicBody(StaticBody):
    """Represents the physics of a dynamic body"""

    # Physical constants

    MIN_BOUNCE_VELOCITY = 2

    def __init__(
        self,
        position: Vector,
        shape,
        orientation,
        texture,
        mass: float,
        elasticity: float = 0,
        friction: float = 0,
        gravity_magnitude: float = 0,
    ):
        """[summary]

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
        super().__init__(position, shape, orientation, texture)
        self.mass = mass
        self.elasticity = elasticity
        self.friction = friction
        self.gravity_magnitude = gravity_magnitude

    def accelerate(self, magnitude_x, magnitude_y):
        self.accel_x += magnitude_x
        self.accel_y += magnitude_y

    def gravity(self):
        self.accelerate(0, self.gravity_magnitude)

    def apply_force(self, force_x, force_y):
        self.accel_x += force_x * self.mass
        self.accel_y += force_y * self.mass

    def get_x_force(self):
        return self.accel_x * self.mass

    def get_y_force(self):
        return self.accel_y * self.mass

    def friction_x(self, x_velo, prev_x, temp_friction_x):
        # TODO: implement friction formulas: Friction(max) = normal reaction * friction coefficient and logic
        # governing friction inheritance
        pass

    def friction_x(self, y_velo, prev_y, temp_friction_y):
        # TODO: implement friction formulas: Friction(max) = normal reaction * friction coefficient and logic
        # governing friction inheritance
        pass

    def update(self, *args):
        # TODO: logic to update objects acceleration and velocities
        pass


# noqa
