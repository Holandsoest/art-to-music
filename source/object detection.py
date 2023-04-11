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
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            
            #possitions
            x, y, w, h = cv2.boundingRect(cnt)
            cy = int(y+h/2)
            cx = int(x+w/2)
            pos_label = ("Position: ({}, {})".format(cx, cy))
            

            #color

            # _, frame = cap.read()
            # hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # if cy > 479 :
            #     cy = 479

            # if cx > 639:
            #     cx = 639
            # pixel_center = hsv_frame[cy, cx]
            # hue_value = pixel_center[0]
            # #type of colors
            # color = "Undefined"
            # if hue_value < 5:
            #     color = "RED"
            # elif hue_value < 22:
            #     color = "ORANGE"
            # elif hue_value < 33:
            #     color = "YELLOW"
            # elif hue_value < 78:
            #     color = "GREEN"
            # elif hue_value < 131:
            #     color = "BLUE"
            # elif hue_value < 170:
            #     color = "VIOLET"
            # else:
            #     color = "RED"

            
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

def detect_shapes_with_contour(contours, image):
    """
    This function goes over all contours that have been read with cv2 
    and will detect all the shapes that would have otherwise been marked as a 'circle'.
    - contours: all contours read with cv2.contours
    Returns nothing.
    """
    # Create shape list_of_shapes
    list_of_shapes = []

    # # Custom Object Detection
    jason_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = os.path.join(os.getcwd(), 'dataset', 'models', 'koen-best.pt')

    #Get the height, width and channel of the image
    img_height, img_width, channel = image.shape
    img_size = img_height*img_width

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
    shape_detector.setJsonPath(jason_path)
    shape_detector.loadModel()

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
    annotate_detected_colors(img, detected_objects)

    cv2.imshow("", img)
    cv2.waitKey()


    
def detect_shapes_with_contour(contours, image):
    """
    This function goes over all contours that have been read with cv2 
    and will detect all the shapes that would have otherwise been marked as a 'circle'.
    - contours: all contours read with cv2.contours
    Returns nothing.
    """
    # Create shape list_of_shapes
    list_of_shapes = []

    # # Custom Object Detection
    jason_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = os.path.join(os.getcwd(), 'dataset', 'models', 'koen-best.pt')

    #Get the height, width and channel of the image
    img_height, img_width, channel = image.shape
    img_size = img_height*img_width

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
    shape_detector.setJsonPath(jason_path)
    shape_detector.loadModel()

    

    def get_image_from_box(contour, img):
        """
        This function gives back just an image of one shape of the picture
        - contour: contour of the shape in the image
        - img: the whole image
        
        Returns just an image of one shape of the whole picture
        """
        x,y,w,h = cv2.boundingRect(contour)
        s_img = img[y:y+h,x:x+w] 
        img_path = 'files\image_processing\example_white_background.jpg'
        l_img = cv2.imread(img_path)
        x_offset=y_offset=500
        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img

        # cv2.imshow("", l_img)
        # cv2.waitKey()
        # img_grayscaled = cv2.cvtColor(l_img, cv2.COLOR_BGR2GRAY)
        # return img_grayscaled
        return l_img


    def detect_shape_with_ai(box):
        """
        This function detects a shape out of a given image, this image should only contain one shape
        - box: is an image of one shape 
        
        Returns "empty" if nothing is detected, else it will detect the name of the shape.
        """
        # cv2.imshow("", box)
        # print("press esc to continue...")
        # cv2.waitKey()
        img, obj = shape_detector.detectObjectsFromImage(input_image=box, 
                                                        output_type="array",
                                                        display_percentage_probability=True,
                                                        display_object_name=True)
        if not obj:
            return "empty"
        else:
            cv2.putText(img, "color_label", (10, 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return obj[0]["name"]

    counter = 0
    for contour in contours:
        area1 = cv2.contourArea(contour)

        if area1 > 100:
            # Get approx contour of shape
            approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

            # minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
            # It will create a rectangle around the shapes
            box = cv2.minAreaRect(contour)
            (x, y), (width, height), angle = box
            shape_size_to_volume = ip.get_volume_from_size(width*height, img_size)
            shape_colorcode_to_bpm = ip.get_bpm_from_color(int(x),int(y),image)
            shape_width_to_duration = ip.get_duration_from_width(width, img_width)
            shape_height_to_pitch = ip.get_volume_from_size(height, img_height)
            shape = i_prop.Image(0, int(shape_size_to_volume), int(shape_colorcode_to_bpm), int(shape_width_to_duration), int(shape_height_to_pitch))

            if len(approx) == 3:
                # Shape is a triangle
                shape.instrument = "triangle"

            elif len(approx) == 4 : 
                x2, y2 , w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                if aspect_ratio >= 0.95 and aspect_ratio < 1.05:
                    shape.instrument = "square"
                    # Shape is a square
                else:
                    shape.instrument = "rectangle"
                    # Shape is a rectangle

            elif len(approx) == 10 :
                # Shape is a star
                shape.instrument = "star"

            else:
                # Shape is half circle, circle or heart
                shape_name = detect_shape_with_ai(get_image_from_box(contour, image))
                if shape_name == "empty":
                    counter+=1
                    continue
                else: 
                    shape.instrument = shape_name
                # Run camera in loop

            list_of_shapes.append(shape)
        else:
            continue

    print("counter: ", counter)
    for shape in list_of_shapes:
        print("instrument:", shape.instrument, "volume:", shape.volume, "bpm:", shape.bpm, "pitch:", shape.pitch, "duration:", shape.duration, sep='\t')

    print("total amount of shapes detected: ", len(list_of_shapes))

def get_color(img:cv2.Mat) -> str:
    """
    function to detect the most common color of an object
    It has one parameter:
    - img: the object that the function should go through
    
    Returns what color the object mainly has
    """
    # Convert image to HSV color space
    # hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Convert image to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color range for red, green, and blue
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([15, 255, 255])
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    lower_violet = np.array([140, 50, 50])
    upper_violet = np.array([160, 255, 255])
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for each color range
    yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    orange_mask = cv2.inRange(hsv_img, lower_orange, upper_orange)
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv_img, lower_blue, upper_blue)
    violet_mask = cv2.inRange(hsv_img, lower_violet, upper_violet)
    red_mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Count the number of pixels in each mask
    yellow_pixels = cv2.countNonZero(yellow_mask)
    orange_pixels = cv2.countNonZero(orange_mask)
    green_pixels = cv2.countNonZero(green_mask)
    blue_pixels = cv2.countNonZero(blue_mask)
    violet_pixels = cv2.countNonZero(violet_mask)
    red_pixels = cv2.countNonZero(red_mask)

    # Determine the dominant color based on the number of pixels
    if yellow_pixels > orange_pixels and yellow_pixels > green_pixels and yellow_pixels > blue_pixels and yellow_pixels > violet_pixels and yellow_pixels > red_pixels:
        return 'yellow'
    elif orange_pixels > yellow_pixels and orange_pixels > green_pixels and orange_pixels > blue_pixels and orange_pixels > violet_pixels and orange_pixels > red_pixels:
        return 'orange'
    elif green_pixels > yellow_pixels and green_pixels > orange_pixels and green_pixels > blue_pixels and green_pixels > violet_pixels and green_pixels > red_pixels:
        return 'green'
    elif blue_pixels > yellow_pixels and blue_pixels > orange_pixels and blue_pixels > green_pixels and blue_pixels > violet_pixels and blue_pixels > red_pixels:
        return 'blue'
    elif violet_pixels > yellow_pixels and violet_pixels > orange_pixels and violet_pixels > green_pixels and violet_pixels > blue_pixels and violet_pixels > red_pixels:
        return 'violet'
    else:
        return 'red'

def annotate_detected_colors(img:cv2.Mat, detected_objects) -> None:
    obj_last = []
    for obj in detected_objects:
        x1, y1, x2, y2 = obj["box_points"]
        obj_img = img[y1:y2, x1:x2]

        # Call function to extract color data
        color = get_color(obj_img)
        obj["color"] = color
        if obj_last:
            if obj_last["name"] == obj["name"] and obj_last["color"] == obj["color"] and obj_last["percentage_probability"] == obj["percentage_probability"]:
                continue
            else:
                # Color label text
                color_label = ("Color: " + color)
                # adding a text to the object 
                cv2.putText(img, color_label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else: 
            # Color label text
            color_label = ("Color: " + color)
            # adding a text to the object 
            cv2.putText(img, color_label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        obj_last = obj

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