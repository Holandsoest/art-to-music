from enum import StrEnum
from enum import IntEnum

class ColorType(IntEnum):
    VIOLET = 60
    BLUE = 75
    YELLOW = 90
    ORANGE = 105
    RED = 120
    GREEN = 135

class ShapeType(StrEnum):
    CIRCLE = "piano"
    HALF_CIRCLE = "flute"
    SQUARE = "drum"
    RECTANGLE = "drum"
    HEART = "violin"
    STAR = "guitar"
    TRIANGLE = "saxophone"
    EMPTY = ""

class Shape:
    """ Class with shape information"""
    def __init__(self, shape, counter, instrument:ShapeType, size, color:ColorType, x_axis, y_axis, box):
        """Initialize shape attributes.
        
        Args:
            shape (str): The shape.
            counter (int): Counter for how many shapes were detected.
            instrument (str): The name of the instrument.
            size (int): The size related to the volume (0-255).
            color (int): The color related to the BPM (60-120, steps of 15).
            x_axis (float): The placement of the note in the bar (0-4, steps of 0.25).
            y_axis (float): The middle point of the shape recalculated to an int (0-100).
            box (tuple): The box around the shape (x1, y1, x2, y2).
        """ 
        self.shape = shape
        self.counter = counter
        self.instrument = instrument
        self.volume = size
        self.bpm = color
        self.note_placement = x_axis
        self.pitch = y_axis
        self.box = box
