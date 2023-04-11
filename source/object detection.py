# Follow this guide: https://imageai.readthedocs.io/en/latest/ 
# This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
# This code contains code for activating webcam. Everything commented out is code for object class detection
# Yet to be added processing for the color, the object size size..

# Things to add. Color to BPM


from imageai.Detection import ObjectDetection # For AI object detection AI
import cv2 # library for the webcam ( this one probably can also find color)
import numpy as np 
import mido
from mido import Message
from mido import MidiFile #for loading midi files
import pandas as pd
import os

from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import image_processing as ip
import common.image_properties as i_prop
from enum import Enum

from imageai.Detection import ObjectDetection

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",159,255,empty)
cv2.createTrackbar("Threshold2","Parameters",53,255,empty)
cv2.createTrackbar("Area","Parameters",10000,30000,empty)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img, imgContour):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        # print(area)#oppervlakte van de figuren
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area>areaMin:
            
            #total points of ervery figure
            
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            
            #possitions
            x, y, w, h = cv2.boundingRect(cnt)
            cy = int(y+h/2)
            cx = int(x+w/2)
            pos_label = ("Position: ({}, {})".format(cx, cy))
            

            #color

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

            
            #extra parts
            #pixel_center_bgr = frame[cy, cx]
            #b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
            #cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
            #cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
            # cv2.circle(imgContour, (x, y),5, (x+w,y+h), (25, 25, 25), 2)

            # cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour, pos_label, (x + w +20, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.putText(imgContour, "color: " +  color, (x + w +20, y + 40), 0, 0.5, (0,255,0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w +20, y + 80), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)

            if len(approx) == 3:
                cv2.putText(imgContour, "Triangle", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            elif len(approx) == 4 : 
                aspect_ratio = float(w)/h
                if aspect_ratio >= 0.95 and aspect_ratio < 1.05:
                    cv2.putText(imgContour, "Square", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)
                else:  
                    cv2.putText(imgContour, "Rectangle", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)

            
            elif len(approx) == 10 :
                # Shape is a star
                cv2.putText(imgContour, "Star", (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)

            else :
                cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)

                
if __name__ == "__main__":
    #----------- AI OBJECT DETECTION --------------------

    # Initialize object detection model
    obj_detect = ObjectDetection()
    #obj_detect.setModelTypeAsYOLOv3()
    obj_detect.setModelTypeAsTinyYOLOv3()
    obj_detect.setModelPath(r"D:\BeCreative\Music based on Art\shape\tiny-yolov3.pt")
    obj_detect.loadModel()
    #-------------------------------------------------------

    # Set webcam parameters
    # cam_feed = cv2.VideoCapture(0)
    # cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    while True:
        ret, img = cap.read()
        imgcamm, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
                                                                   display_percentage_probability=False,
                                                                   display_object_name=True)
        

        
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



        _, imageFrame = cap.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        success, img = cap.read()

        threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")

        imgContour = img.copy()
        imgBlur = cv2.GaussianBlur(img,(7,7),0)
        imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
        imgCanny = cv2.Canny(imgGray,threshold1,threshold2)

        kernel = np.ones((5,5))
        imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
        
        getContours(imgDil,imgcamm)

        
        imgStack = stackImages(0.8,([imgContour]))
        # cv2.imshow("Result", imgStack)
        cv2.imshow("ai", imgcamm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    

    # cam_feed.release()
    # cv2.destroyAllWindows()
    # outport.close()