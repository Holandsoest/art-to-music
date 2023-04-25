# Follow this guide: https://imageai.readthedocs.io/en/latest/ 
# This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import cv2 
import numpy as np 
import os
import image_processing as ip
import common.image_properties as img_prop
from enum import Enum

# Function to get the color of an object in the image
def get_color(img:cv2.Mat) -> str:
    """
    function to detect the most common color of an object
    It has one parameter:
    - img: the object that the function should go through
    
    Returns what color the object mainly has
    """
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
    
def detect_shapes_with_ai(image):
    """
    Function to detect shapes via AI\n
    Input:
    - image: the image loaded in via opencv2

    Returns annotated image.    
    """
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
    
    annotate_detected_colors(img, detected_objects)
    return img
    
def detect_shapes_with_contour(contours, image):
    """
    This function goes over all contours that have been read with cv2 
    and will detect all the shapes that would have otherwise been marked as a 'circle'.
    - contours: all contours read with cv2.contours

    Returns an image and a list with details of all the shapes on the image.
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
        
        Returns an image of one shape of the whole picture
        """
        x,y,w,h = cv2.boundingRect(contour)
        s_img = img[y:y+h,x:x+w] 
        img_path = 'files\image_processing\example_white_background_960x560.jpg'
        l_img = cv2.imread(img_path)
        x_offset=y_offset=50
        l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
        return l_img


    def detect_shape_with_ai(box):
        """
        This function detects a shape out of a given image, this image should only contain one shape
        - box: is an image of one shape 
        
        Returns the name of the shape, if no shape detected it will return "empty"
        """
        img, obj = shape_detector.detectObjectsFromImage(input_image=box, 
                                                        output_type="array",
                                                        display_percentage_probability=True,
                                                        display_object_name=True)
        annotate_detected_colors(img, obj)
        # cv2.imshow("img", img)
        if not obj:
            cv2.imshow("empty shape", box)
            cv2.waitKey()
            cv2.destroyAllWindows()
            return "empty"
        else:
            # cv2.putText(img, "color_label", (10, 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return obj[0]["name"]
        
    counter = 0
    # cv2.drawContours(image, contours, -1, (255,0,0), 3)
    for contour in contours:
        counter += 1
        area1 = cv2.contourArea(contour)

        # area_min = cv2.getTrackbarPos("Area", "Parameters")
        # if area1 > area_min:
        if area1 > 50:
            # Get approx contour of shape
            # Now you can use this function to approximate the shape. 
            # In this, second argument is called epsilon, which is maximum distance from contour to approximated contour. 
            # It is an accuracy parameter. 
            # A wise selection of epsilon is needed to get the correct output.
            epsilon = 0.05*cv2.arcLength(contour,True)
            approx = cv2.approxPolyDP(contour,epsilon,True)
            # approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

            # minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
            # It will create a rectangle around the shapes
            rect = cv2.minAreaRect(contour)

            (x,y),radius = cv2.minEnclosingCircle(contour)
            center = (int(x),int(y))
            radius = int(radius)
            cv2.circle(image,center,radius,(0,255,0),1)

            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(image,[box],0,(0,0,255),1)
            (x, y), (width, height), angle = rect


            shape_size_to_volume = ip.get_volume_from_size(width*height, img_size)
            shape_colorcode_to_bpm = ip.get_bpm_from_color(int(x),int(y),image)
            shape_width_to_duration = ip.get_duration_from_width(width, img_width)
            shape = img_prop.Image("", counter, 0, int(shape_size_to_volume), int(shape_colorcode_to_bpm), int(shape_width_to_duration), 0)

            if len(approx) == 3:
                # Shape is a triangle (Guitar)
                shape.shape = "triangle"
                shape.instrument = "guitar"
                shape.pitch = int(ip.get_pitch_from_size(height, img_height, "guitar"))
                # cv2.drawContours(image, contour, -1, (255,0,0), 1)
            elif len(approx) == 4 : 
                x2, y2 , w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                if aspect_ratio >= 0.95 and aspect_ratio < 1.05:
                    shape.shape = "square"
                    shape.instrument = "drum"
                    shape.pitch = int(ip.get_pitch_from_size(height, img_height, "drum"))
                    # Shape is a square (Drum Pads)
                    # cv2.drawContours(image, contour, -1, (255,0,0), 1)
                else:
                    shape.shape = "rectangle"
                    shape.instrument = "drum"
                    shape.pitch = int(ip.get_pitch_from_size(height, img_height, "drum"))
                    # cv2.drawContours(image, contour, -1, (255,0,0), 1)
                    # Shape is a rectangle (Drum Pads)

            elif len(approx) == 10 :
                # Shape is a star (Cello)
                shape.shape = "star"
                shape.instrument = "cello"
                shape.pitch = int(ip.get_pitch_from_size(height, img_height, "cello"))
                # cv2.drawContours(image, contour, -1, (255,0,0), 1)
            else:
                # Shape is half circle, circle or heart
                shape_name = detect_shape_with_ai(get_image_from_box(contour, image))
                if shape_name == "empty":
                    shape.pitch = int(ip.get_pitch_from_size(height, img_height, "empty"))
                    # cv2.drawContours(image, contour, -1, (0,255,0), 1)
                    
                    continue
                else: 
                    shape.shape = shape_name
                    if shape_name == "half circle":
                        shape_name = "flute"
                        # cv2.drawContours(image, contour, -1, (255,255,0), 1)
                    elif shape_name == "heart": 
                        shape_name = "piano"
                        # cv2.drawContours(image, contour, -1, (255,0,255), 1)
                    elif shape_name == "circle":
                        shape_name = "violin"
                        # cv2.drawContours(image, contour, -1, (0,255,255), 1)
                    elif shape_name == "square":
                        shape_name = "drum"
                    elif shape_name == "traingle":
                        shape_name = "guitar"
                    elif shape_name == "star":
                        shape_name = "cello"
                        # cv2.drawContours(image, contour, -1, (0,0,255), 1)
                    shape.instrument = shape_name
                    shape.pitch = int(ip.get_pitch_from_size(height, img_height, shape_name))

            list_of_shapes.append(shape)
        else:
            continue

    for shape in list_of_shapes:
        print(shape.counter, 
              "shape:", shape.shape, 
              "instrument:", shape.instrument, 
              "volume:", shape.volume, 
              "bpm:", shape.bpm, 
              "pitch:", shape.pitch, 
              "duration:", shape.duration, 
              sep='\t')

    return image, list_of_shapes

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
            # Adding a text to the object 
            cv2.putText(img, color_label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        obj_last = obj

class ModelSelection(Enum):
    """An enum of different choices.  
    - `ORIGINAL_MODEL`  Is the downloaded `tiny-yolov3` model. It can detect kites.  
    - `PREVIOUS_STABLE` A model is stable when the trainer person has validated that it is the current best; this is the previous one.  
    - `STABLE`          A model is stable when the trainer person has validated that it is the current best.  
    - `LATEST`          The model that was most recently made. Latest models might constantly change.  
    - `CUSTOM`          Change the paths below here to quickly test another model or json."""
    # ORIGINAL_MODEL = 0
    # PREVIOUS_STABLE = 1
    # STABLE = 2
    LATEST = 3
    CUSTOM = 4
model_paths = {
    # ModelSelection.ORIGINAL_MODEL:  os.path.join(os.getcwd(), 'files', 'image_processing_ai', 'tiny-yolov3.pt'),
    # ModelSelection.STABLE:          os.path.join(os.getcwd(), 'dataset', 'models', 'tiny-yolov3_dataset_mAP-0.98251_epoch-18.pt'),
    ModelSelection.LATEST:          os.path.join(os.getcwd(), 'dataset', 'models', 'tiny-yolov3_dataset_last.pt'),
    ModelSelection.CUSTOM:          os.path.join(os.getcwd(), 'dataset', 'models', 'tiny-yolov3_dataset_mAP-0.85113_epoch-7.pt'),
}

def load_custom_model(path) -> CustomObjectDetection:
    """Loads the model and the Json and returns the `shape_detector`"""
    json_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_path = path

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_path)
    shape_detector.setJsonPath(json_path)
    shape_detector.loadModel()
    return shape_detector

def train_custom_model():
    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsTinyYOLOv3()
    dataset_path = os.path.join(os.getcwd(), 'dataset')
    trainer.setDataDirectory(data_directory=dataset_path)
    trainer.setTrainConfig(object_names_array=["circle", "half circle", "square", "heart", "star", "triangle"]
                           ,batch_size=2
                           ,num_experiments=30
                           ,train_from_pretrained_model=os.path.join(os.getcwd(), 'files', 'image_processing_ai', 'tiny-yolov3.pt')
                           )
    trainer.trainModel()
    
def compare_all_models(img:cv2.Mat|None, path:str|None) -> None:
    """Opens the image as it looks for each model, (and original), can also give a path to a folder with pictures instead and it will do all the pictures"""
    
    # Make a list with all images
    images = []
    if isinstance(img, cv2.Mat): images.append(img)
    if os.path.exists(path):
        for file in os.listdir(path):
            if file.find('.jpg') == -1: continue
            images.append(cv2.imread(os.path.join(path,file)))
    if len(images) < 1: raise FileExistsError("Told me to compare models with images, but you gave me no valid images.") 

    # Make a list with all models
    model_paths = []
    for file in os.listdir(os.path.join(os.getcwd(),'dataset','models')):
        if file.find('.pt') == -1: continue
        model_paths.append(os.path.join(os.getcwd(),'dataset','models',file))

    for image in images:
        cv2.imshow(f'No model',image)
        for model_path in model_paths:
            shape_detector = load_custom_model(model_path)
            annotated, detected_objects = shape_detector.detectObjectsFromImage(input_image=image,
                                                                                    output_type="array",
                                                                                    display_percentage_probability=True,
                                                                                    display_object_name=True)
            annotate_detected_colors(img=annotated, detected_objects=detected_objects)
            cv2.imshow(f'Model: "{os.path.split(model_path)[1]}"',annotated)
        print('Press `esc` for the next')
        while(not (cv2.waitKey(20) & 0xFF ==27)):pass# Break the loop when user hits 'esc' key