from imageai.Detection import ObjectDetection # For AI object detection AI
import cv2 # library for the webcam ( this one probably can also find color)

cap = cv2.VideoCapture(0)
             
if __name__ == "__main__":

    obj_detect = ObjectDetection()
    obj_detect.setModelTypeAsTinyYOLOv3()
    obj_detect.setModelPath(r"D:\BeCreative\Music based on Art\shape\tiny-yolov3.pt")
    obj_detect.loadModel()

    while True:
        ret, img = cap.read()
        imgcamm, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
                                                                   display_percentage_probability=False,
                                                                   display_object_name=True)

        _, imageFrame = cap.read()

        cv2.imshow("ai", imgcamm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    



######################################################
