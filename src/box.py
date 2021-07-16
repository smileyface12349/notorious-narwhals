import curses
import heapq
from functools import total_ordering
from typing import Any, List, NoReturn

from .datatypes.game_object import GameObject


@total_ordering
class ZSortMixin:
    """Mixin to provide sorting by z-value"""

    __slots__ = ()

    def __lt__(self, other: Any):
        """Lesser then cmp function"""
        return self.z < other.z


# Import GameObject class when it is done


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
        # TODO: Iterate through each object
        #   For each object, work out which object(s) are touching it
        #       Then, call object.update()

    def render(self, screen: curses.window) -> NoReturn:
        """Renders the contents of the box"""
        if len(self.objects) == 0:
            return  # There is nothing to render!

        for obj in self.objects:
            self._render_object(obj, screen)

        # screen.update() ?

    def _render_object(self, obj: GameObject, screen: curses.window) -> NoReturn:
        """
        Renders object on the screen (character-by-character)

        It doesn't affect performance because curses draws all the stuff at once
        when screen.update() is called (or when .getkey() / .getch() is called)
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
                    draw(pos.y, pos.x, char, colour)

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
