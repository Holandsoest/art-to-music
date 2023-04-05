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

# Function to get the color of an object in the image
# def get_color(img):
#     # Convert image to HSV color space
#     # hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
#     # Define color range for red, green, and blue
#     # lower_yellow = np.array([20, 100, 100], np.uint8)
#     # upper_yellow = np.array([30, 255, 255], np.uint8)
#     # yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
#     # yellow_mask = cv2.dilate(yellow_mask, kernel)
#     # print(hsv_img)


#     # lower_orange = np.array([5, 100, 100], np.uint8)
#     # upper_orange = np.array([15, 255, 255], np.uint8)

#     # lower_green = np.array([36, 25, 25])
#     # upper_green = np.array([86, 255, 255])

#     # lower_blue = np.array([110, 50, 50])
#     # upper_blue = np.array([130, 255, 255])

#     # lower_violet = np.array([140, 50, 50])
#     # upper_violet = np.array([160, 255, 255])

#     # lower_red1 = np.array([0, 50, 50])
#     # upper_red1 = np.array([10, 255, 255])

#     # lower_red2 = np.array([170, 50, 50])
#     # upper_red2 = np.array([180, 255, 255])
#     red_lower = np.array([136, 87, 111], np.uint8)
#     red_upper = np.array([180, 255, 255], np.uint8)
#     red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
  
#     green_lower = np.array([25, 52, 72], np.uint8)
#     green_upper = np.array([102, 255, 255], np.uint8)
#     green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
  
#     blue_lower = np.array([94, 80, 2], np.uint8)
#     blue_upper = np.array([120, 255, 255], np.uint8)
#     blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

#     kernel = np.ones((5, 5))      
#     # Create masks for each color range

#     # orange_mask = cv2.inRange(hsv_img, lower_orange, upper_orange)
#     # green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
#     # blue_mask = cv2.inRange(hsv_img, lower_blue, upper_blue)
#     # violet_mask = cv2.inRange(hsv_img, lower_violet, upper_violet)
#     # red_mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
#     # red_mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
#     # red_mask = cv2.bitwise_or(red_mask1, red_mask2)

  
#     # Count the number of pixels in each mask
#     red_pixels = cv2.dilate(red_mask, kernel)
#     green_pixels = cv2.dilate(green_mask, kernel)
#     blue_pixels = cv2.dilate(blue_mask, kernel)
#     # blue_pixels = cv2.countNonZero(blue_mask)
#     # violet_pixels = cv2.countNonZero(violet_mask)
#     # red_pixels = cv2.countNonZero(red_mask)
    
#     # Determine the dominant color based on the number of pixels
#     if red_pixels():
#         return 'red'
#     elif green_pixels():
#         return 'orange'
#     elif blue_pixels():
#         return 'green'
#     # elif blue_pixels > yellow_pixels and blue_pixels > orange_pixels and blue_pixels > green_pixels and blue_pixels > violet_pixels and blue_pixels > red_pixels:
#     #     return 'blue'
#     # elif violet_pixels > yellow_pixels and violet_pixels > orange_pixels and violet_pixels > green_pixels and violet_pixels > blue_pixels and violet_pixels > red_pixels:
#     #     return 'violet'
#     # else:
#     #     return 'red'


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
    cam_feed = cv2.VideoCapture(0)
    cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    # Open port and map notes to objects
    # outport = mido.open_output()
    # track_map = {
    #     "person": "1.mid",   # send MIDI file 1 chosen
    #     "cell phone": "2.mid",      # send MIDI file 2 chonsen
    #     "cup": "3.mid",      # send MIDI file 3 chosen
    #     # This will be changed by names of shapes
    # }

    # Run camera in loop
    while True:
        ret, img = cam_feed.read()
        # _, imageFrame = cam_feed.read()
        # hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        # Object detection parametres
        annotated_image, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
                                                                   display_percentage_probability=False,
                                                                   display_object_name=True)
        # Loop through detected objects and add color information
        for obj in preds:
            x, y, w, h = obj["box_points"]


            pos_label = ("Position: ({}, {})".format(x, y))
            cv2.putText(annotated_image, pos_label, (x + w +20, y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cy = int(y+h/2)
            cx = int(x+w/2)
            _, frame = cam_feed.read()
            
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

            # cv2.putText(annotated_image, color, (x + w +20, y + 50), 0, 0.5, (0,255,0), 2)
            cv2.putText(annotated_image, color, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2)

            pos_label = ("Position: ({}, {})".format(x, y))
            # adding text to the object 
            #cv2.putText(annotated_image, color_label, (x1, y1-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.putText(annotated_image, size_label, (x1, y1-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(annotated_image, pos_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # Loop through detected objects and send MIDI messages
        # for obj in preds:
        #     obj_name = obj["name"].lower()
        #     if obj_name in track_map:
        #         file_name = track_map[obj_name]
        #         mid = MidiFile(file_name)
        #         for msg in mid.play():
        #             outport.send(msg)

        cv2.imshow("", annotated_image)
        # Exit loop if user presses 'q' key or 'Esc' key
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            break

    cam_feed.release()
    cv2.destroyAllWindows()
    # outport.close()

