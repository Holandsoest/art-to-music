import math
import common.image_properties as img_prop
import cv2
import numpy as np

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
        return img_prop.ColorType.YELLOW
    elif orange_pixels > yellow_pixels and orange_pixels > green_pixels and orange_pixels > blue_pixels and orange_pixels > violet_pixels and orange_pixels > red_pixels:
        return img_prop.ColorType.ORANGE
    elif green_pixels > yellow_pixels and green_pixels > orange_pixels and green_pixels > blue_pixels and green_pixels > violet_pixels and green_pixels > red_pixels:
        return img_prop.ColorType.GREEN
    elif blue_pixels > yellow_pixels and blue_pixels > orange_pixels and blue_pixels > green_pixels and blue_pixels > violet_pixels and blue_pixels > red_pixels:
        return img_prop.ColorType.BLUE
    elif violet_pixels > yellow_pixels and violet_pixels > orange_pixels and violet_pixels > green_pixels and violet_pixels > blue_pixels and violet_pixels > red_pixels:
        return img_prop.ColorType.VIOLET
    else:
        return img_prop.ColorType.RED

def get_placement_of_note(x_axis_middlepoint, img_width) -> int | float:
    """
    This function finds the ratio between the middle point of a shape and the total image width.
    It takes two arguments:
    - x_axis: the x_axis middle_point of the shape in the image
    - img_width: the width of the entire image
    
    It returns a scaled value between 0 and 4 based on the ratio of x_axis to img_width in steps of 0.25
    """
    ratio = x_axis_middlepoint / img_width
    scaled_value = min(math.ceil(ratio * 16) / 4, 4.0)
    return scaled_value

def get_volume_from_size(obj_size, img_size) -> int:
    """
    This function scales the size of an object in an image relative to the size of the entire image.img_size
    It takes two arguments:
    - obj_size: the size of the object in pixels
    - img_size: the size of the entire image in pixels
    
    It returns a scaled value between 20 - 255 based on the ratio of obj_size to img_size.
    It starts at 20 otherwise the smaller objects wouldn't even make a sound.
    """
    return min((((obj_size)+(img_size*0.7))/img_size)*255, 255)

def get_pitch_from_y_axis(y_axis, img_height) -> int:
    """
    This function scales the y_axis to the image height
    It takes two arguments:
    - y_axis: the size of the object
    - img_height: the size of the entire image
    
    It returns a scaled value between 0 - 100
    """
    return (100 - ((y_axis/img_height)*100))

def display_list_of_shapes(list_of_shapes) -> None:
    for shape in list_of_shapes:
        print(shape.counter, 
              "shape:", shape.shape, 
              "instrument:", shape.instrument, 
              "volume:", shape.volume, 
              "bpm:", shape.bpm, 
              "pitch:", shape.pitch, 
              "note_placement:", shape.note_placement, 
              sep='\t')