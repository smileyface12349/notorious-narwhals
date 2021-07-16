from ...datatypes import GameObject


class Wall(GameObject):
    """A static object that does not move"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static = True
