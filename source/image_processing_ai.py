# Follow this guide: https://imageai.readthedocs.io/en/latest/ 
# This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import cv2 
import numpy as np 
import os
from enum import Enum
import common.image_properties as img_prop
import image_processing as img_proc

shape_detector = CustomObjectDetection()

def setup_ai():
    # # Custom Object Detection
    jason_path = os.path.join(os.getcwd(), 'dataset', 'json', 'dataset_tiny-yolov3_detection_config.json')
    model_custom_path = os.path.join(os.getcwd(), 'dataset', 'models', 'dataset_version_mAP-0.63917.pt')

    shape_detector.setModelTypeAsTinyYOLOv3()
    shape_detector.setModelPath(model_custom_path)
    shape_detector.setJsonPath(jason_path)
    shape_detector.loadModel()

def correct_boxes(img:cv2.Mat, detected_objects): # -> image, boxpoints
    boxes = []
    boxes_w_names = []

    def non_max_suppression(boxes, boxes_w_names, overlapThresh = 0.4): # -> boxpoints
        """
        Function to determine non maximum suppression
        Inputs:
        - boxes: all the boxes detected by ai or contours.
        - overlapThresh: the threshold of boxes overlapping.
        
        Return all the bouding boxes that are double
        """
        # if there are no boxes, return an empty list
        if len(boxes) == 0:
            return []
        
        # if the bounding boxes integers, convert them to floats --
        # this is important since we'll be doing a bunch of divisions
        if boxes.dtype.kind == "i":
            boxes = boxes.astype("float")

        # initialize the list of picked indexes	
        pick = []

        # grab the coordinates of the bounding boxes
        x1 = boxes[:,0]
        y1 = boxes[:,1]
        x2 = boxes[:,2]
        y2 = boxes[:,3]

        # compute the area of the bounding boxes and sort the bounding
        # boxes by the bottom-right y-coordinate of the bounding box
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)

        area_descend = (x2 - x1 + 1) * (y2 - y1 + 1)
        area_descend[::-1].sort()

        # keep looping while some indexes still remain in the indexes list
        while len(idxs) > 0:
            # grab the last index in the indexes list and add the
            # index value to the list of picked indexes
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            # find the largest (x, y) coordinates for the start of
            # the bounding box and the smallest (x, y) coordinates
            # for the end of the bounding box
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])

            # compute the width and height of the bounding box
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            # compute the ratio of overlap
            overlap = (w * h) / area[idxs[:last]]

            # delete all indexes from the index list that have
            idxs = np.delete(idxs, np.concatenate(([last],
                np.where(overlap > overlapThresh)[0])))
            
        # return only the bounding boxes that were picked using the
        # integer data type
        return boxes_w_names[pick]

    for obj in detected_objects:
        x1, y1, x2, y2 = obj["box_points"]
        box_name = obj["name"]

        bounding_box_w_names = [int(x1), int(y1), int(x2), int(y2), str(box_name)]
        bounding_box = [int(x1), int(y1), int(x2), int(y2)]
        boxes.append(bounding_box)
        boxes_w_names.append(bounding_box_w_names)

    boxes_w_names = np.array(boxes_w_names)
    boxes = np.array(boxes)
    double_boxes = non_max_suppression(boxes, boxes_w_names)

    for obj in double_boxes:
        x1 = obj[0]
        y1 = obj[1]
        x2 = obj[2] 
        y2 = obj[3]
        box_name = obj[4]

        # Adding a text to the object 
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0), 2)
    
    return img, double_boxes
    
def detect_shapes_with_ai(image): # -> image, list
    """
    Function to detect shapes via AI
    Input:
    - image: the image loaded in via opencv2

    Returns annotated image.    
    """
    list_of_shapes = []
    img_height, img_width, channel = image.shape
    img_size = img_height*img_width

    img, detected_objects = shape_detector.detectObjectsFromImage(input_image=image, 
                                                                output_type="array",
                                                                minimum_percentage_probability=60,
                                                                display_percentage_probability=True,
                                                                display_object_name=True)
    img, boxes = correct_boxes(image, detected_objects)

    for counter, box in enumerate (boxes):
        x1, y1, x2, y2, box_name = box

        middle_point_x = (int(x1)+int(x2))/2
        middle_point_y = (int(y1)+int(y2))/2

        width = int(x2) - int(x1)
        height = int(y2) - int(y1)

        obj_img = img[int(y1):int(y2), int(x1):int(x2)]
        color_code = img_proc.get_color(obj_img)

        shape_ai = img_prop.Shape("", 
                                  counter, 
                                  0, 
                                  int(img_proc.get_volume_from_size(width*height, img_size)), 
                                  color_code, 
                                  float(img_proc.get_placement_of_note(middle_point_x, img_width)), 
                                  int(img_proc.get_pitch_from_y_axis(middle_point_y, img_height)), 
                                  (int(x1), int(y1), int(x2), int(y2)) )
        shape_ai.shape = box_name
        cv2.putText(img, str(counter), (int(middle_point_x), int(middle_point_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (125, 0, 0), 2)

        if box_name == "circle":
            shape_ai.instrument = img_prop.ShapeType.CIRCLE
        elif box_name == "half circle":
            shape_ai.instrument = img_prop.ShapeType.HALF_CIRCLE
        elif box_name == "square":
            shape_ai.instrument = img_prop.ShapeType.SQUARE
        elif box_name == "heart": 
            shape_ai.instrument = img_prop.ShapeType.HEART
        elif box_name == "star":
            shape_ai.instrument = img_prop.ShapeType.STAR
        elif box_name == "triangle":
            shape_ai.instrument = img_prop.ShapeType.TRIANGLE
        else:
            shape_ai.instrument = img_prop.ShapeType.EMPTY
        list_of_shapes.append(shape_ai)

    return img, list_of_shapes
   
def annotate_detected_colors(img:cv2.Mat, detected_objects) -> None:
    obj_last = []
    for obj in detected_objects:
        x1, y1, x2, y2 = obj["box_points"]
        obj_img = img[y1:y2, x1:x2]

        # Call function to extract color data
        color = img_proc.get_color(obj_img)
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

def train_custom_model() -> None:
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