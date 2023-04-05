#Follow this guide: https://imageai.readthedocs.io/en/latest/ 
#This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import cv2 
import numpy as np 
import os
import image_processing as ip
from enum import Enum

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
def load_custom_model(model_selection:ModelSelection) -> CustomObjectDetection:
    """Loads the model and the Json and returns the `shape_detector`"""
    json_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = model_paths[model_selection]

    shape_detector = CustomObjectDetection()
    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
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
def compare_all_models(img:cv2.Mat) -> None:
    """Opens the image as it looks for each model, (and original)"""
    cv2.imshow(f'No model',img)
    for model_selection in ModelSelection:
        shape_detector = load_custom_model(model_selection)
        annotated, detected_objects = shape_detector.detectObjectsFromImage(input_image=img,
                                                                                   output_type="array",
                                                                                   display_percentage_probability=True,
                                                                                   display_object_name=True)
        annotate_detected_colors(img=annotated, detected_objects=detected_objects)
        cv2.imshow(f'Model: "{model_selection.name}"',annotated)

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
    img_path = 'files\image_processing\example_shapes (2).jpg'
    img = cv2.imread(img_path)

    train_custom_model()
    compare_all_models(img)

    # Put image into AI and color detection
    # shape_detector = load_custom_model(ModelSelection.LATEST)
    # annotated, detected_objects = shape_detector.detectObjectsFromImage(input_image=img,
    #                                                                             output_type="array",
    #                                                                             display_percentage_probability=True,
    #                                                                             display_object_name=True)
    # annotate_detected_colors(img=annotated, detected_objects=detected_objects)
    # cv2.imshow(f'Model: ',annotated)


    # Display to user
    print('Press `esc` to close...')
    while(not (cv2.waitKey(20) & 0xFF ==27)):pass# Break the loop when user hits 'esc' key
    cv2.destroyAllWindows()