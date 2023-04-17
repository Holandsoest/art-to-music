import cv2
import image_processing as img_proc
import common.midi_creation as mc
import image_processing_ai as img_proc_ai
from imageai.Detection import ObjectDetection
import numpy as np 
#
cap = cv2.VideoCapture(0)
#

if __name__ == "__main__":


    while(1):
        

        ret, img = cap.read()
        shapes = img_proc.get_contours_from_image(img)         
        img_proc_ai.detect_shapes_with_contour(shapes, img)
        img_proc_ai.detect_shapes_with_ai(img)

        cv2.imshow("met detectie", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    

        # Break the loop when user hits 'esc' key 
        # if cv2.waitKey(20) & 0xFF ==27:
        #     print('Enjoy the music')
        #     break
        
    # cv2.destroyAllWindows()

    # mc.MakeSong(list_of_shapes)