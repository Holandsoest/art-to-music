class Image:
    def __init__(shape, name, size, color, x_axis, y_axis):
        #name is an integer related to instrument, 
        #see: https://www.midi.org/specifications-old/item/gm-level-1-sound-set
        shape.instrument = name
        #volume is integer between 20 - 100 (change to 0 - 255)
        shape.volume = size
        #bpm is an int with table of 30 with a max of 240
        shape.bpm = color
        #duration is the x_axis middle point of the shape recalculated to an int between 1 - 4
        shape.duration = x_axis
        #pitch is the y_axis middle point of the shape recalculated to an int between 0 - 255
        shape.pitch = y_axis