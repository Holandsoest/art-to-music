import cv2
import numpy as np
# import pandas as pd

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

def get_pitch_from_size(obj_height, img_height, shape_name):
    """
    This function scales the size of an object in an image relative to the size of the entire image.img_size
    It takes two arguments:
    - obj_size: the size of the object in pixels
    - img_size: the size of the entire image in pixels
    
    It returns a scaled value between 20 - 255 based on the ratio of obj_size to img_size.
    It starts at 20 otherwise the smaller objects wouldn't even make a sound.
    """
    match shape_name:
        case "guitar":
            # represents a (triangle) guitar, the pitch of this instrument should be in between 74 and 96
            return min((((obj_height)+(img_height*0.74))/img_height)*96, 96)
        
        case "drum":
            # represents a (square / rectangle) drumpads, the pitch of this instrument should be in between 69 and 86
            return min((((obj_height)+(img_height*0.69))/img_height)*86, 86)
        
        case "cello":
            # represents a (star) cello, the pitch of this instrument should be in between 48 and 77
            return min((((obj_height)+(img_height*0.48))/img_height)*77, 77)
        
        case "flute":
            # represents a (half circle) flute, the pitch of this instrument should be in between 72 and 108
            return min((((obj_height)+(img_height*0.2))/img_height)*108, 108)
        
        case "piano":
            # represents a (heart) piano, the pitch of this instrument should be in between 0 and 100   
            return min((((obj_height)+(img_height))/img_height)*100, 100)
        
        case "violin":
            # represents a (circle) violin, the pitch of this instrument should be in between 76 and 103
            return min((((obj_height)+(img_height*0.76))/img_height)*103, 103)
        
        case "empty":
            return 0

def get_contours_from_image(image):
    """
    This function reads an image using the OpenCV library and detects contours in the image using the Hough transform algorithm. 
    It takes one argument:
    - image: an image read with OpenCV library.

    The function returns a all the contours detected in the image
    """
    # aperture_size = 5
    # L2Gradient = True

    # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

    # img_blur = cv2.GaussianBlur(image, (3,3), 0)
    # img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # Canny makes the whole picture black and white 
    # img_canny = cv2.Canny(img_gray, threshold1, threshold2, L2gradient = L2Gradient )

    # # A kernel(a matrix of odd size(3,5,7) is convolved with the image.
    # # A pixel in the original image (either 1 or 0) will be considered 1 only if all the pixels under the kernel are 1, otherwise, it is eroded (made to zero).
    # # Thus all the pixels near the boundary will be discarded depending upon the size of the kernel.
    # # So the thickness or size of the foreground object decreases or simply the white region decreases in the image.
    # kernel = np.ones((5,5))
    # img_dil = cv2.dilate(img_canny, kernel, iterations = 1)
    
    # contours, hierarchy = cv2.findContours(img_dil, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Reading the image with opencv
    img_grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # add img_blur if you make use of jpg files
    # img_blur = cv2.blur(img_grayscaled, (3,3))

    ret , thrash = cv2.threshold(img_grayscaled, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def setup_contour():
    def empty(a):
        pass

    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 240)
    cv2.createTrackbar("Threshold1", "Parameters", 159, 255, empty)
    cv2.createTrackbar("Threshold2", "Parameters", 53, 255, empty)
    cv2.createTrackbar("Area", "Parameters", 0, 200, empty)
