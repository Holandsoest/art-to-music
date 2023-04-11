import cv2
import pandas as pd
import os
import common.image_properties as ip

def get_bpm_from_color(x_axis, y_axis, image):
    """
    This function gets the RGB values of a pixel on the (x,y)-coordinates of an image and scales this to a number of the table of 30.
    It takes three arguments:
    - x_axis: the x axis coordinate of the pixel
    - y_axis: the y axis coordinate of the pixel
    - image:  the image that will be scanned for the pixel
    
    It returns a scaled value of the table of 30. This number will represent the beats per minute(BPM) of the instrument.
    """
    b, g, r = image[y_axis, x_axis]
    b = int(b)
    g = int(g)
    r = int(r)

    # # For now the rgb colorcode will represent a bpm match, but later on we will probably work with colorname to bpm
    # def get_shape_color(R,G,B):
    #         #Reading csv file with pandas and giving names to each column
    #     index=["color","color_name","hex","R","G","B"]
    #     absolute_path = os.path.join(os.getcwd(), 'files','image_processing', 'colors.csv')
    #     csv = pd.read_csv(absolute_path, names=index, header=None)

    #     minimum = 10000
    #     for i in range(len(csv)):
    #         d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
    #         if(d<=minimum):
    #             minimum = d
    #             cname = csv.loc[i,"color_name"]
    #     return cname
    
    # colorName = get_shape_color(r,g,b)

    def round_up_to_30(number):
        return min(((number + 29) // 30) * 30, 240)
    
    bpm = round_up_to_30((b + g + r) / 3)
    if bpm < 30:
        return 30
    else:
        return bpm

def get_duration_from_width(obj_width, img_width):
    """
    This function scales the width of an object in an image relative to the width of the entire image.
    It takes two arguments:
    - obj_width: the width of the object in pixels
    - img_width: the width of the entire image in pixels
    
    It returns a scaled value between 1 and 4 based on the ratio of obj_width to img_width.
    """
    ratio = obj_width / img_width
    if ratio < 0.25:
        return 1
    elif ratio < 0.5:
        return 2
    elif ratio < 0.75:
        return 3
    else:
        return 4

def get_volume_from_size(obj_size, img_size):
    """
    This function scales the size of an object in an image relative to the size of the entire image.img_size
    It takes two arguments:
    - obj_size: the size of the object in pixels
    - img_size: the size of the entire image in pixels
    
    It returns a scaled value between 20 - 255 based on the ratio of obj_size to img_size.
    It starts at 20 otherwise the smaller objects wouldn't even make a sound.
    """
    return min((((obj_size)+(img_size*0.2))/img_size)*255, 255)

def get_contours_from_image(image):
    """
    This function reads an image using the OpenCV library and detects contours in the image using the Hough transform algorithm. 
    It takes one argument:
    - image: an image read with OpenCV library.

    The function returns a all the contours detected in the image
    """
    #Reading the image with opencv
    img_grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret , thrash = cv2.threshold(img_grayscaled, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    print("amount of contours: ", len(contours))
    return contours


# def read_image(image):
#     """
#     This function reads an image using the OpenCV library and detects shapes in the image using the Hough transform algorithm. 
#     It takes one argument:
#     - image: an image read with OpenCV library.

#     The function returns a list of Image objects, each representing a shape in the image with properties such as volume, pitch, duration, and beats per minute (BPM).
#     """
#     #Create shape list_of_shapes
#     list_of_shapes = []

#     #Reading the image with opencv
#     img_grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     #Get the height, width and channel of the image
#     img_height, img_width, channel = image.shape
#     img_size = img_height*img_width

#     ret , thrash = cv2.threshold(img_grayscaled, 240 , 255, cv2.CHAIN_APPROX_NONE)
#     contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#     #Go through all the contours/shapes that are detected
#     for contour in contours:
#         #Get approx contour of shape
#         approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

#         #minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
#         #It will create a rectangle around the shapes
#         box = cv2.minAreaRect(contour)
#         (x, y), (width, height), angle = box
#         shape_size_to_volume = get_volume_from_size(width*height, img_size)
#         shape_colorcode_to_bpm = get_bpm_from_color(int(x),int(y),image)
#         shape_width_to_duration = get_duration_from_width(width, img_width)
#         shape_height_to_pitch = get_volume_from_size(height, img_height)
#         shape = ip.Image(0, int(shape_size_to_volume), int(shape_colorcode_to_bpm), int(shape_width_to_duration), int(shape_height_to_pitch))

#         if len(approx) == 3:
#             #Triangle = Guitar sound = number 30
#             shape.instrument = 30

#         elif len(approx) == 4 : 
#             x2, y2 , w, h = cv2.boundingRect(approx)
#             aspect_ratio = float(w)/h
#             if aspect_ratio >= 0.95 and aspect_ratio < 1.05:
#                 #Square = Drum = number 119
#                 shape.instrument = 119
#             else:
#                 # #Rectangle (representing a half circle) = flute = number 74
#                 shape.instrument = 74

#         elif len(approx) == 5 :
#             #Pentagon (representing a heartshape) = piano = 2
#             shape.instrument = 2

#         elif len(approx) == 10 :
#             #Star = Cello = 43
#             shape.instrument = 43

#         else:
#             #Circle = lead 1 = 81
#             shape.instrument = 81
        
#         list_of_shapes.append(shape)

#     # Accessing object value using a for loop
#     for shape in list_of_shapes:
#         print("instrument:", shape.instrument, "volume:", shape.volume, "bpm:", shape.bpm, "pitch:", shape.pitch, "duration:", shape.duration, sep='\t')

#     return list_of_shapes, contours




