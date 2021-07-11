import curses
from typing import NoReturn

# Defining colors based on objects` properties
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Regular
curses.init_pair(2, 121, curses.COLOR_BLACK)  # Sticky
curses.init_pair(3, 111, curses.COLOR_BLACK)  # Icy (little to no friction)
curses.init_pair(4, 228, curses.COLOR_BLACK)  # Bouncy


class BoxState:
    """Defines the current state of the box. Has a render() method to display the contents"""

    def __init__(self):
        self.objects = []

    def clear(self) -> NoReturn:
        """Clears the box of all objects"""
        self.objects = []

    def add_object(self, added_object) -> NoReturn:
        """Adds an object to the objects list"""
        self.objects.append(added_object)

    def render(self, screen: curses.window) -> NoReturn:
        """Renders the contents of the box"""
        if len(self.objects) == 0:
            return  # There is nothing to render!

        for obj in sorted(self.objects, key=lambda x: x.z):  # Sorts objects by their Z depth
            if obj.override_colors:  # If the object decides to override default property-based colors:
                curses.init_pair(100, *obj.color)
                color = curses.color_pair(100)
            else:
                # We're sorting if statements by importance. An object being bouncy is the most important,
                # therefore we're making it the top if statement.

                if obj.elasticity >= 0.6:  # If the object is bouncy
                    color = curses.color_pair(4)
                elif obj.friction == 1:  # If an object has a friction of 1, it's sticky.
                    color = curses.color_pair(2)
                elif obj.friction <= 0.3:
                    color = curses.color_pair(3)
                else:  # If it's just a regular ol' object.
                    color = curses.color_pair(1)

            # Drawing stuff on the screen character-by-character
            # It doesn't affect performance because curses draws all the stuff at once
            # when screen.update() is called (or when .getkey() / .getch() is called)
            for x in range(obj.size[0]):
                for y in range(obj.size[1]):
                    draw_pos_x = obj.position[0] + x
                    draw_pos_y = obj.position[1] + y

                    # Giant if statement to decide if we should draw the tile
                    if (draw_pos_x >= 0 and draw_pos_x < screen.getmaxyx()[1]) and (
                        draw_pos_y >= 0 and draw_pos_y < screen.getmaxyx()[0]
                    ):
                        screen.insch(draw_pos_y, draw_pos_x, "@", color)
