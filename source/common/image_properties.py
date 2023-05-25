class Shape:
    """ Class with shape information"""
    def __init__(self, shape, counter, name, size, color, x_axis, y_axis, box):
        """Initialize shape attributes.

        Args:
            shape (str): The shape.
            counter (int): Counter for how many shapes were detected.
            name (str): The name of the instrument.
            size (int): The size related to the volume (0-255).
            color (int): The color related to the BPM (60-120, steps of 15).
            x_axis (float): The placement of the note in the bar (0-4, steps of 0.25).
            y_axis (float): The middle point of the shape recalculated to an int (0-100).
            box (tuple): The box around the shape (x1, y1, x2, y2).
        """
        self.shape = shape
        self.counter = counter
        self.instrument = name
        self.volume = size
        self.bpm = color
        self.note_placement = x_axis
        self.pitch = y_axis
        self.box = box

        x1, y1, x2, y2 = box
        middle_point_x = (x1+x2)/2
        middle_point_y = (y1+y2)/2
        self.middlepoint = (middle_point_x, middle_point_y)
