from typing import NoReturn


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
