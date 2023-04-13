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

    obj_detect = ObjectDetection()
    #obj_detect.setModelTypeAsYOLOv3()
    obj_detect.setModelTypeAsTinyYOLOv3()
    obj_detect.setModelPath(r"D:\BeCreative\Music based on Art\shape\tiny-yolov3.pt")
    obj_detect.loadModel()


    while(1):
        

        ret, img = cap.read()
        imgcamm, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
                                                                   display_percentage_probability=False,
                                                                   display_object_name=True)
        


        shapes = img_proc.get_contours_from_image(imgcamm)         
        img_proc_ai.detect_shapes_with_contour(shapes, imgcamm)
        img_proc_ai.detect_shapes_with_ai(imgcamm)

        _, imageFrame = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    

        # Break the loop when user hits 'esc' key 
        # if cv2.waitKey(20) & 0xFF ==27:
        #     print('Enjoy the music')
        #     break
        
    # cv2.destroyAllWindows()

    # mc.MakeSong(list_of_shapes)