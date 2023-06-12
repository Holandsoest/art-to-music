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
    cv2.imshow('Camera', img)

    image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)

    midi_creation.MakeSong(list_of_shapes)
    print('success')
    midi_processing.AudiRenderPlugin(list_of_shapes)
    print('stuck')

    # TODO: play audio with pygame

    cv2.waitKey(0)
    cv2.destroyAllWindows()
