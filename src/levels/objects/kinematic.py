import sys

sys.path.append("..")

from src.datatypes import GameObject  # noqa: E402


class FallingObject(GameObject):
    """Falls, but doesn't bounce. Can be any shape"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mass = 1
