class Image:
    def __init__(self, shape, counter, name, size, color, x_axis, y_axis, box):
        """ 
        Class for shape information
        Inputs:
        - shape:    the shape (str)
        - counter:  counter for how many shapes detected
        - name:     name is an integer related to instrument, 
                    see: https://www.midi.org/specifications-old/item/gm-level-1-sound-set
        - size:     relates to the volume, this is an integer between 20 - 100 (change to 0 - 255)
        - color:    relates to the bpm, this is an int with table of 60 - 120. steps of 15
        - x_axis:   relates to the placement of the note in the bar. Number between 0 - 4 steps of 0.25
        - y_axis:   relates to the pitch, this is the y_axis middle point of the shape 
                    recalculated to an int between 0 - 255
        - box:      this is the box around the shape (x1, y1, x2, y2)

        Returns: None
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