import cv2
import numpy as np
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import take_image

img_proc_ai.setup_ai()

if __name__ == "__main__":
    # TODO: Do this when jetson button press
    
    img = take_image.get_image()
    print(' here')
    cv2.imshow('Camera', img)
    print(' here')

    image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)
    print(' here')

    midi_creation.MakeSong(list_of_shapes)
    print(' here')
    midi_processing.AudiRenderPlugin(list_of_shapes)
    print(' here')

    # TODO: play audio with pygame

    cv2.waitKey(0)
    cv2.destroyAllWindows()
