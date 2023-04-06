#Follow this guide: https://imageai.readthedocs.io/en/latest/ 
#This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import cv2 
import numpy as np 
import os
import image_processing as ip
import common.image_properties as i_prop

# Function to get the color of an object in the image
def get_color(img):
    """
    function to detect the most common color of an object
    It has one parameter:
    - img: the object that the function should go through
    It will return what color the object mainly has
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
    
def detect_shapes_with_contour(contours, image):
    """
    This function goes over all contours that have been read with cv2 
    and will detect all the shapes that would have otherwise been marked as a 'circle'.
    - contours: all contours read with cv2.contours

    The function returns nothing.
    """
    #Create shape list_of_shapes
    list_of_shapes = []

    # # Custom Object Detection
    jason_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = os.path.join(os.getcwd(), 'dataset', 'models', 'tiny-yolov3_dataset_mAP-0.98251_epoch-18.pt')

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
    shape_detector.setJsonPath(jason_path)
    shape_detector.loadModel()

    def get_image_from_box(c, img):
        x,y,w,h = cv2.boundingRect(c) 
        if w>50 and h>50: 
            return img[y:y+h,x:x+w] 
        else:
            return 0

    def detect_shape(box):
        if isinstance(box, int):
            return "empty"
        img, obj = shape_detector.detectObjectsFromImage(input_image=box, 
                                                        output_type="array",
                                                        display_percentage_probability=True,
                                                        display_object_name=True)
        if not obj:
            return "empty"
        else:
            cv2.putText(img, "color_label", (10, 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return obj[0]["name"]

    for contour in contours:
        # Get approx contour of shape
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

        # minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
        # It will create a rectangle around the shapes
        box = cv2.minAreaRect(contour)
        shape = i_prop.Image(0, 0, 0, 0, 0)

        (x, y), (width, height), angle = box
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
            shape_name = detect_shape(get_image_from_box(contour, image))
            if shape_name == "empty":
                continue
            else: 
                shape.instrument = shape_name
            # Run camera in loop

        list_of_shapes.append(shape)

    for shape in list_of_shapes:
        print("instrument:", shape.instrument, "volume:", shape.volume, "bpm:", shape.bpm, "pitch:", shape.pitch, "duration:", shape.duration, sep='\t')

            


def detect_shapes_with_ai(img):
    """
    This function reads an image using AI with the Yolov3 library
    - image: an image read with OpenCV library.

    The function returns nothing.
    """
    # # Custom Object Detection
    jason_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = os.path.join(os.getcwd(), 'dataset', 'models', 'tiny-yolov3_dataset_mAP-0.98251_epoch-18.pt')

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
    shape_detector.setJsonPath(jason_path)
    shape_detector.loadModel()

    # # Set webcam parameters
    # cam_feed = cv2.VideoCapture(0)
    # cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
    # cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)

    # # Trainer model
    # model_path = os.path.join(os.getcwd(), 'files', 'image_processing_ai', 'tiny-yolov3.pt')
    # trainer = DetectionModelTrainer()
    # trainer.setModelTypeAsTinyYOLOv3()
    # dataset_path = os.path.join(os.getcwd(), 'dataset')
    # trainer.setDataDirectory(data_directory=dataset_path)
    # trainer.setTrainConfig(object_names_array=["circle", "half circle", "square", "heart", "star", "triangle"]
    #                        ,batch_size=4
    #                        ,num_experiments=100
    #                        ,train_from_pretrained_model=model_path
    #                        )
    # trainer.trainModel()

    # Run camera in loop
    while True:
        # ret, img = cam_feed.read()

    # Object detection parametres
        annotated_image, preds = shape_detector.detectObjectsFromImage(input_image=img, 
                                                                       output_type="array",
                                                                       display_percentage_probability=True,
                                                                       display_object_name=True)

        # Loop through detected objects and add color information
        for obj in preds:
            x1, y1, x2, y2 = obj["box_points"]
            obj_img = img[y1:y2, x1:x2]
            # ip.readImage(obj_img)
            # Call function to extract color data
            color = get_color(obj_img)
            obj["color"] = color
            # Color lable text
            color_label = ("Color: " + color)
            # adding a text to the object 
            cv2.putText(annotated_image, color_label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
        cv2.imshow("Annotated Image", annotated_image)
        # Exit loop if user presses 'q' key or 'Esc' key
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            break

    # # cam_feed.release()
    # cv2.destroyAllWindows()