import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np
#import image_processing as img_proc
#import common.midi_creation as midi_creation
#import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import take_image 

img_proc_ai.setup_ai()

if __name__ == "__main__":
    img = take_image.get_image()
    image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)

    cv2.imshow('Camera', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # if __name__ == "__main__":
        
    #     while(1):
    #         img = camera.read()
    #         status = camera.hasError()
    #         print(status)
    #         #success, img = cap.read()
    

    #         # img_proc.display_list_of_shapes(list_of_shapes)
    #         # midi_creation.MakeSong(list_of_shapes)
    #         # midi_processing.AudiRenderPlugin(list_of_shapes)

    #         if cv2.waitKey(20) & 0xFF == ord('q'):
    #             break
    #cap.release()
   # cv2.destroyAllWindows()
