#Follow this guide: https://imageai.readthedocs.io/en/latest/ 
#This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import cv2 
import numpy as np 
import os
import image_processing as ip
from enum import Enum
import time

# Function to get the color of an object in the image
def get_color(img:cv2.Mat) -> str:
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
def annotate_detected_colors(img:cv2.Mat, detected_objects) -> None:
    for obj in detected_objects:
        x1, y1, x2, y2 = obj["box_points"]
        obj_img = img[y1:y2, x1:x2]

        # Call function to extract color data
        color = get_color(obj_img)
        obj["color"] = color
        
        # Color label text
        color_label = ("Color: " + color)
        # adding a text to the object 
        cv2.putText(img, color_label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

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
def train_custom_model(epochs:int, batch_size:int):
    """Trains the model with the data provided in the folders
    ---
    - `epochs` [> 2] int, how many times the trainer may ajust the model
    - `batch_size` [> 1] int, how many images should be run trough the ai in parallel
    """
    batch_size = max(2, batch_size)
    epochs = max(3, epochs)

    dataset_path = os.path.join(os.getcwd(), 'dataset')

    amount_of_data = len(os.listdir(os.path.join(dataset_path, 'train', 'annotations'))) + len(os.listdir(os.path.join(dataset_path, 'validation', 'annotations')))
    

    print(f'Start training:\n\t{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}\n\t{epochs} epochs\t{batch_size} batch_size')
    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsTinyYOLOv3()
    trainer.setDataDirectory(data_directory=dataset_path)
    trainer.setTrainConfig(object_names_array=["circle", "half circle", "square", "heart", "star", "triangle"]
                           ,batch_size=batch_size
                           ,num_experiments=epochs
                           ,train_from_pretrained_model=os.path.join(os.getcwd(), 'files', 'image_processing_ai', 'tiny-yolov3.pt')
                           )
    trainer.trainModel()
    print(f'Stopped training:\n\t{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}')
def compare_all_models(img:cv2.Mat|None, image_path:str|None, has_colors:bool) -> None:
    """Opens the image as it looks for each model, (and original), can also give a path to a folder with pictures instead and it will do all the pictures"""
    
    # Make a list with all images
    images = []
    if isinstance(img, cv2.Mat): images.append(img)
    if os.path.exists(image_path):
        for file in os.listdir(image_path):
            if file.find('.png') == -1: continue
            images.append(cv2.imread(os.path.join(image_path,file)))
    if len(images) < 1: raise FileExistsError("Told me to compare models with images, but you gave me no valid images.") 

    # Make a list with all models
    model_paths = []
    for file in os.listdir(os.path.join(os.getcwd(),'dataset','models')):
        if file.find('.pt') == -1: continue
        model_paths.append(os.path.join(os.getcwd(),'dataset','models',file))

    for image in images:
        # cv2.imshow(f'No model',image)
        for model_path in model_paths:
            shape_detector = load_custom_model(model_path)
            annotated, detected_objects = shape_detector.detectObjectsFromImage(input_image=image,
                                                                                    output_type="array",
                                                                                    display_percentage_probability=True,
                                                                                    display_object_name=True)
            if has_colors: annotate_detected_colors(img=annotated, detected_objects=detected_objects)
            cv2.imshow(f'Model: "{os.path.split(model_path)[1]}"',annotated)
        print('Press the any key for the next image')
        cv2.waitKey()

def detect_shapes(img): ## OLD CODE
    # Custom Object Detection
    shape_detector = load_custom_model(ModelSelection.LATEST)

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
        annotated_image, detected_objects = shape_detector.detectObjectsFromImage(input_image=img, 
                                                                       output_type="array",
                                                                       display_percentage_probability=True,
                                                                       display_object_name=True)

        # Loop through detected objects and add color information
        for obj in detected_objects:
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

        # for obj in detected_objects:
        #     x1, y1, x2, y2 = obj["box_points"]
        #     obj_img = img[y1:y2, x1:x2]
        #     # Call function to extract color data
        #     color = get_color(obj_img)
        #     obj["color"] = color
        #     # Color lable text
        #     color_label = ("Color: " + color)
        #     # Calculate size of box
        #     size = (x2 - x1) * (y2 - y1)
        #     # Size label text
        #     size_label = ("Size: " + str(size))
        #     # Position label text
        #     pos_label = ("Position: ({}, {})".format(x1, y1))
        #     # adding text to the object 
        #     cv2.putText(annotated_image, color_label, (x1, y1-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #     cv2.putText(annotated_image, size_label, (x1, y1-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #     cv2.putText(annotated_image, pos_label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
        # cv2.imshow("Annotated Image", annotated_image)
        # # Exit loop if user presses 'q' key or 'Esc' key
        # if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
        #     break

    # # cam_feed.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    # Training settings
    epochs = 4
    batch_size = 20
    training_count = len(os.listdir(os.path.join(os.getcwd(),'dataset','train','annotations')))
    validation_count = len(os.listdir(os.path.join(os.getcwd(),'dataset','validation','annotations')))
    estimation_duration = round( 4*training_count*epochs/30000/14   +   training_count/250000.0*2.25, 1)
    estimated_completion = round( estimation_duration + time.localtime().tm_hour + time.localtime().tm_min/60.0 ,1)
    print(f'Training the AI with {epochs}epochs and a batch_size of {batch_size}\nWith {training_count} training images and {validation_count} validation images\nIs estimated to take Brosha ~{estimation_duration} hours...\nEstimation reads to be done at ~{estimated_completion}\nScared?\n')
    train_custom_model(epochs, batch_size)
    

    # compare_all_models(img=None,
    #                    image_path=os.path.join(os.getcwd(),'files','image_processing_ai','manual_validation','500'),
    #                    has_colors=False)
    compare_all_models(img=None,
                       image_path=os.path.join(os.getcwd(),'files','image_processing_ai','manual_validation','1000'),
                       has_colors=False)

    # Display to user
    cv2.destroyAllWindows()
