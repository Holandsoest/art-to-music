class Image:
    def __init__(self, shape, counter, name, size, color, x_axis, y_axis):
        #shape
        self.shape = shape
        #counter for the shapes.
        self.counter = counter
        #name is an integer related to instrument, 
        #see: https://www.midi.org/specifications-old/item/gm-level-1-sound-set
        self.instrument = name
        #volume is integer between 20 - 100 (change to 0 - 255)
        self.volume = size
        #bpm is an int with table of 30 with a max of 240
        self.bpm = color
        #duration is the x_axis middle point of the shape recalculated to an int between 1 - 4
        self.duration = x_axis
        #pitch is the y_axis middle point of the shape recalculated to an int between 0 - 255
        self.pitch = y_axis