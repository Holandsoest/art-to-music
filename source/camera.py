# Follow this guide: https://imageai.readthedocs.io/en/latest/ 
# This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
# This code contains code for activating webcam. Everything commented out is code for object class detection
# Yet to be added processing for the color, the object size size..

# Things to add. Color to BPM
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import cv2 
import numpy as np 
import os
import image_processing as ip
import common.image_properties as i_prop
from enum import Enum

from imageai.Detection import ObjectDetection # For AI object detection AI
import cv2 # library for the webcam ( this one probably can also find color)
import numpy as np 

cap = cv2.VideoCapture(0)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",35,255,empty)
cv2.createTrackbar("Threshold2","Parameters",53,255,empty)
cv2.createTrackbar("Area","Parameters",2000,30000,empty)

def detect_shapes_with_ai(image):
    contours = ip.get_contours_from_image(image)
    amount_of_contours = len(contours)
    # # Custom Object Detection
    jason_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = os.path.join(os.getcwd(), 'dataset', 'models', 'koen-best.pt')

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
    shape_detector.setJsonPath(jason_path)
    shape_detector.loadModel()

    img, detected_objects = shape_detector.detectObjectsFromImage(input_image=image, 
                                                    output_type="array",
                                                    display_percentage_probability=True,
                                                    display_object_name=True)
    
    print("amount of detected objects: ", len(detected_objects))
    # annotate_detected_colors(img, detected_objects)

    cv2.imshow("aiiii", img)


def points(contours, imgContour,x,y,w,h):
    peri = cv2.arcLength(contours,True)
    approx = cv2.approxPolyDP(contours,0.02*peri,True)
    if len(approx) == 3:
        cv2.putText(imgContour, "Triangle", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
        cv2.drawContours(imgContour, contours, -1, (255, 0, 0), 3)
    elif len(approx) == 4 : 
        aspect_ratio = float(w)/h
        if aspect_ratio >= 0.95 and aspect_ratio < 1.05:
            cv2.putText(imgContour, "Square", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
            cv2.drawContours(imgContour, contours, -1, (255, 0, 0), 3)
        else:  
            cv2.putText(imgContour, "Rectangle", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
            cv2.drawContours(imgContour, contours, -1, (255, 0, 0), 3)

    
    elif len(approx) == 10 :
        # Shape is a star
        cv2.putText(imgContour, "Star", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
        cv2.drawContours(imgContour, contours, -1, (255, 0, 0), 3)

    else :
        cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
        detect_shapes_with_ai(img)
        cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)

def color(imgContour, x,y,w,h,cy,cx):
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if cy > 479 :
        cy = 479

    if cx > 639:
        cx = 639
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]
    #type of colors
    color = "Undefined"
    if hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"
    # cv2.putText(imgContour, "color: " +  color, (x + w +20, y + 40), 0, 0.5, (0,255,0), 2)


def posiont(imgContour,x,y,w,h):
    cy = int(y+h/2)
    cx = int(x+w/2)
    pos_label = ("Position: ({}, {})".format(cx, cy))
    # cv2.putText(imgContour, pos_label, (x + w +20, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    color(imgContour, x,y,w,h,cy,cx)



def getContours(imgContour):


    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")

    imgBlur = cv2.GaussianBlur(img,(7,7),0)
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)

    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
    
    contours,hierarchy = cv2.findContours(imgDil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        # print(area)#oppervlakte van de figuren
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area>areaMin:
            x, y, w, h = cv2.boundingRect(cnt)
            #total points of ervery figure
            
            points(cnt, imgContour,x,y,w,h)
            #possitions
            
            posiont(imgContour,x,y,w,h)
            #color


            # cv2.putText(imgContour, "Area: " + str(int(area)), (x + w +20, y + 80), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
            #extra parts
            #pixel_center_bgr = frame[cy, cx]
            #b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
            #cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
            #cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
            # cv2.circle(imgContour, (x, y),5, (x+w,y+h), (25, 25, 25), 2)

            # cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)


                
if __name__ == "__main__":
    #----------- AI OBJECT DETECTION --------------------

    # # Initialize object detection model
    # obj_detect = ObjectDetection()
    # #obj_detect.setModelTypeAsYOLOv3()
    # obj_detect.setModelTypeAsTinyYOLOv3()
    # obj_detect.setModelPath(r"D:\BeCreative\Music based on Art\shape\tiny-yolov3.pt")
    # obj_detect.loadModel()
    #-------------------------------------------------------

    # Set webcam parameters
    # cam_feed = cv2.VideoCapture(0)
    # cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    while True:
        ret, img = cap.read()
        # imgcamm, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
        #                                                            display_percentage_probability=False,
        #                                                            display_object_name=True)
        

        
        # contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        


        # for obj in preds:
        #     x, y, w, h = obj["box_points"]
        #     cy = int(y+h/2)
        #     cx = int(x+w/2)
        #     pos_label = ("Position: ({}, {})".format(cx, cy))
        #     _, frame = cam_feed.read()
        #     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #     if cy > 479 :
        #         cy = 479

        #     if cx > 639:
        #         cx = 639

        #     pixel_center = hsv_frame[cy, cx]
        #     hue_value = pixel_center[0]

        #     color = "Undefined"
        #     if hue_value < 5:
        #         color = "RED"
        #     elif hue_value < 22:
        #         color = "ORANGE"
        #     elif hue_value < 33:
        #         color = "YELLOW"
        #     elif hue_value < 78:
        #         color = "GREEN"
        #     elif hue_value < 131:
        #         color = "BLUE"
        #     elif hue_value < 170:
        #         color = "VIOLET"
        #     else:
        #         color = "RED"

        #     cv2.putText(annotated_image, color, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2)
        #     cv2.putText(annotated_image, pos_label, (x , y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
        # detect_shapes_with_ai(img)
        getContours(img)
        
        
        # imgStack = stackImages(0.8,([imgContour]))
        # cv2.imshow("Result", imgStack)
        cv2.imshow("ai", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    

    # cam_feed.release()
    # cv2.destroyAllWindows()
    # outport.close()