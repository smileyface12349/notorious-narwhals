import curses
import heapq
import math
from functools import total_ordering
from typing import Any, List, NoReturn

from .datatypes.game_object import GameObject
from .datatypes.vector import window_manager as vector_window_manager


@total_ordering
class ZSortMixin:
    """Mixin to provide sorting by z-value"""

    __slots__ = ()

    def __lt__(self, other: Any):
        """Lesser then cmp function"""
        return self.z < other.z


def init_colors() -> NoReturn:
    """Initialize colors"""
    # Defining colors based on objects` properties
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular
    curses.init_pair(2, 121, curses.COLOR_BLACK)  # Sticky
    curses.init_pair(3, 111, curses.COLOR_BLACK)  # Icy (little to no friction)
    curses.init_pair(4, 228, curses.COLOR_BLACK)  # Bouncy


class BoxState:
    """Defines the current state of the box. Has a render() method to display the contents"""

    _current_color_slot = 49

    def __init__(self, initial_objects: List[GameObject] = None):
        self.objects = []

        if initial_objects is not None:
            # Sorting objects initially to avoid sorting when rendering
            for obj in initial_objects:
                heapq.heappush(self.objects, obj)

    def clear(self) -> NoReturn:
        """Clears the box of all objects"""
        self.objects.clear()

    def add_object(self, obj: GameObject) -> NoReturn:
        """Adds an object to the objects list"""
        heapq.heappush(self.objects, obj)

    def update(self) -> NoReturn:
        """Updates the position of all objects. Should be called every tick"""
        vector_window_manager.update()

        for obj in self.objects:
            obj: GameObject
            # TODO: Right now, this assumes the objects are rectangular. Could do with circles in here
            #   It also does not (fully) support changing orientation
            touching = []
            for coll in self.objects:
                coll: GameObject
                if coll == obj:
                    continue

                # vertical collisions
                if obj.position.y < coll.position.y:  # from above (check bottom edge of coll)
                    result = obj.position.y <= coll.position.y + coll.size.y <= obj.position.y + obj.size.y
                else:  # from below (check top edge of coll)
                    result = obj.position.y <= coll.position.y <= obj.position.y + obj.size.y
                # horizontal collisions
                if not result:
                    if obj.position.x < coll.position.x:  # from left (check right edge of coll)
                        result = obj.position.x <= coll.position.x + coll.size.x <= obj.position.x + obj.size.x
                    else:  # from right (check left edge of coll)
                        result = obj.position.x <= coll.position.x <= obj.position.x + obj.size.x

                if not result:  # if it hasn't collided, we're not interested
                    continue

                min_angle = 90 - math.degrees(
                    math.atan((coll.position.y - obj.position.y) / (coll.position.x - obj.position.x))
                )
                max_angle = 90.0  # this has to be changed to support variable orientations
                plane_normal = 0  # rectangles with no orientation are always flat

                touching.append((min_angle, max_angle, coll, plane_normal))

            obj.update(touching)

    def render(self, screen: curses.window) -> NoReturn:
        """Renders the contents of the box"""
        if len(self.objects) == 0:
            return  # There is nothing to render!

        screen.clear()
        for obj in self.objects:
            self._render_object(obj, screen)
        screen.refresh()

    def _render_object(self, obj: GameObject, screen: curses.window) -> NoReturn:
        """
        Renders object on the screen (character-by-character)

        It doesn't affect performance because curses draws all the stuff at once
        when screen.refresh() is called (or when .getkey() / .getch() is called)
        """
        # color = self._get_object_color(obj)

        buffer = obj.render()
        for pos, char, colour in buffer:
            if (0 <= pos.x < screen.getmaxyx()[1]) and (0 <= pos.y < screen.getmaxyx()[0]):
                if pos.x == screen.getmaxyx()[1] - 1 and pos.y == screen.getmaxyx()[0] - 1:
                    # insch doesn't raise en error when drawing on the bottom right tile
                    draw = screen.insch
                else:
                    draw = screen.addch

                if char != "TRANSPARENT":
                    draw(int(pos.y), int(pos.x), char, colour)

    @staticmethod
    def _get_object_color(obj: GameObject) -> int:
        """Gets the color of an object based on their properties / custom color"""
        if obj.override_colors:  # If the object decides to override default property-based colors:
            # All of this for multiple colors to render simultaneously
            if BoxState._current_color_slot == 256:
                BoxState._current_color_slot = 49

            curses.init_pair(BoxState._current_color_slot, *obj.color)

            BoxState._current_color_slot += 1  # Incrementing it for next iteration

            return curses.color_pair(BoxState._current_color_slot - 1)

        # We're sorting if statements by importance. An object being bouncy is the most important,
        # therefore we're making it the top if statement.
        if obj.elasticity >= 0.6:  # If the object is bouncy
            return curses.color_pair(4)
        elif obj.friction == 1:  # If an object has a friction of 1, it's sticky.
            return curses.color_pair(2)
        elif obj.friction <= 0.3:  # Icy
            return curses.color_pair(3)
        else:  # If it's just a regular ol' object.
            return curses.color_pair(1)
