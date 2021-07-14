import typing
from typing import List, NoReturn

from .vector import Vector

if typing.TYPE_CHECKING:
    from . import GameObject


class Triggers:
    """Represents an output action for a sensor (e.g. button, lever)

    Consists of a list of triggers
    """

    def __init__(self, triggers: List["Trigger"]):
        self.triggers = triggers

    def process(self) -> NoReturn:
        """Process a list of triggers (in order)"""
        for trigger in self.triggers:
            trigger.process()


class Trigger:
    """Represents a single trigger"""

    def process(self) -> NoReturn:
        """Process the trigger. Must be subclassed"""
        pass


class ForceTrigger(Trigger):
    """Represents a trigger involving applying a force to another object"""

    def __init__(self, target: "GameObject", force: Vector):
        self.target = target
        self.force = force

    def process(self) -> NoReturn:
        """Process a force-based trigger"""
        self.target.add_temp_force(self.force)


class CustomTrigger(Trigger):
    """Represents a trigger with no direct action

    The .process() method should be defined manually when initializing the class

    Where possible, it is recommended to create an additional class to provide the functionality required
    """

    def __init__(self, identifier: int, **kwargs):
        self.identifier = identifier
        self.options = kwargs
