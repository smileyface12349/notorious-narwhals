from math import sqrt
from typing import NoReturn
from typing.abc import Callable

from datatypes.vector import Vector


class Drawer:
    """Draws vector shapes on the screen"""

    def __init__(self, buffer_add: Callable[[Vector, str, int], NoReturn]):
        self.buffer_add = buffer_add

    def draw_tile(self, pos: Vector, char: str, colour: int) -> NoReturn:
        """Draws a tile at a position"""
        self.buffer_add(pos, char, colour)

    def draw_line(self, pos1: Vector, pos2: Vector, char: str, colour: int) -> NoReturn:
        """Draws a vector line. Positions are tiles."""
        distance_x = pos2.x - pos1.x
        distance_y = pos2.y - pos1.y

        # Both points are on the same position
        if distance_x == 0 and distance_y == 0:
            self.draw_tile(pos1, char, colour)
            return

        if abs(distance_x) >= abs(distance_y):
            if pos2.x > pos1.x:
                self._draw_line_x(pos1, pos2, char, colour)
            else:
                self._draw_line_x(pos2, pos1, char, colour)

        else:
            if pos2.y > pos1.y:
                self._draw_line_y(pos1, pos2, char, colour)
            else:
                self._draw_line_y(pos2, pos1, char, colour)

    def _draw_line_x(self, pos1: Vector, pos2: Vector, char: str, colour: int) -> NoReturn:
        distance_x = pos2.x - pos1.x
        distance_y = pos2.y - pos1.y

        m = distance_y / distance_x

        for x in range(pos1.x, pos2.x + 1):
            y = m * (x - pos1.x) + pos1.y

            self.draw_tile(Vector(x, y), char, colour)

    def _draw_line_y(self, pos1: Vector, pos2: Vector, char: str, colour: int) -> NoReturn:
        distance_x = pos2.x - pos1.x
        distance_y = pos2.y - pos1.y

        m_inv = distance_x / distance_y

        for y in range(pos1.y, pos2.y + 1):
            x = m_inv * (y - pos1.y) + pos1.x

            self.draw_tile(Vector(x, y), char, colour)

    def draw_rect(self, pos: Vector, size: Vector, char: str, colour: int) -> NoReturn:
        """
        Draws a rectangle

        Float positions are allowed.
        """
        for x in range(round(pos.x), round(pos.x) + size.x, 1):
            for y in range(round(pos.y), round(pos.y) + size.y, 1):
                draw_x = round(pos.x) + x
                draw_y = round(pos.y) + y

                self.draw_tile(Vector(draw_x, draw_y), char, colour)

    def draw_circle(self, pos: Vector, radius: int, char: str, colour: int) -> NoReturn:
        """
        Draws a circle

        Float positions are allowed.
        """
        for x in range(-radius, radius):
            height = round(sqrt(radius * radius - x * x) / 2)

            for y in range(-height, height):
                self.draw_tile(Vector(x + pos.x, y + pos.y), char, colour)
