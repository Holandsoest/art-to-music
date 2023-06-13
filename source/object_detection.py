# Follow this guide: https://imageai.readthedocs.io/en/latest/ 
# This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
# For virtual port Download LoopMidi
# This code contains code for activating webcam. Everything commented out is code for object class detection
# Yet to be added processing for the color, the object size size..

# Things to add. Color to BPM



from imageai.Detection import ObjectDetection # For AI object detection AI
import cv2 # library for the webcam ( this one probably can also find color)
import numpy as np 
import mido
from mido import Message, MidiFile
import threading



# Function to get the color of an object in the image
def get_color(img):
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
def MidiSend():
    obj_name = obj["name"].lower()
    if obj_name in track_map:
        file_name = track_map[obj_name]
        mid = MidiFile(file_name)
        play_time = mid.length
        playing = False  # initialize playing variable outside of the loop
        tick = 0  # initialize tick variable outside of the loop
        for msg in mid.play():
            outport.send(msg)
            playing = True
            tick += msg.time
            if tick >= play_time:  # fix condition for ending the loop
                playing = False
                break  # exit loop if play_time is exceeded


if __name__ == "__main__":
    #----------- AI OBJECT DETECTION --------------------

    # Initialize object detection model
    obj_detect = ObjectDetection()
    #obj_detect.setModelTypeAsYOLOv3()
    obj_detect.setModelTypeAsTinyYOLOv3()
    obj_detect.setModelPath(r"C:\Users\kpelj\OneDrive\Desktop\Uni\Year 4\Minor\WebCamAi\tiny-yolov3.pt")
    obj_detect.loadModel()
    #-------------------------------------------------------

    # Set webcam parameters
    cam_feed = cv2.VideoCapture(0)
    cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
    cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)

    # Open port and map notes to objects
    outport = mido.open_output()
    track_map = {
        "person": "1.mid",   # send MIDI file 1 chosen
        "cell phone": "2.mid",      # send MIDI file 2 chonsen
        "cup": "3.mid",      # send MIDI file 3 chosen
        # This will be changed by names of shapes
    }

    # Run camera in loop
    while True:
        playing = False
        ret, img = cam_feed.read()

        # Object detection parametres
        annotated_image, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
                                                                   display_percentage_probability=False,
                                                                   display_object_name=True)
        # Loop through detected objects and add color information
        for obj in preds:
            x1, y1, x2, y2 = obj["box_points"]
            obj_img = img[y1:y2, x1:x2]
            # Call function to extract color data
            color = get_color(obj_img)
            obj["color"] = color
            # Color lable text
            color_label = ("Color: " + color)
            # Calculate size of box
            size = (x2 - x1) * (y2 - y1)
            # Size label text
            size_label = ("Size: " + str(size))
            # Position label text
            pos_label = ("Position: ({}, {})".format(x1, y1))
            # adding text to the object 
            cv2.putText(annotated_image, color_label, (x1, y1-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(annotated_image, size_label, (x1, y1-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(annotated_image, pos_label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # Loop through detected objects and send MIDI messages
        for obj in preds:
            x = threading.Thread(target=MidiSend)
            x.start()
        cv2.imshow("", annotated_image)
        # Exit loop if user presses 'q' key or 'Esc' key
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            break

    cam_feed.release()
    cv2.destroyAllWindows()
    outport.close()

