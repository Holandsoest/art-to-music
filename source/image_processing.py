import cv2
import numpy as np
import os
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
        
        case _:
            return 0
        
def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def get_contours_from_image(image, threshold_lower, threshold_upper):
    """
    This function reads an image using the OpenCV library and detects contours in the image using the Hough transform algorithm. 
    It takes one argument:
    - image: an image read with OpenCV library.

    The function returns a all the contours detected in the image
    """
    ##### this code for .jpg files
    aperture_size = 3
    L2Gradient = True

    
    img_blur = cv2.GaussianBlur(image, (5,5), 0)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    # Canny explained 
    # Hysteresis: The final step. Canny does use two thresholds (upper and lower):
    # If a pixel gradient is higher than the upper threshold, the pixel is accepted as an edge
    # If a pixel gradient value is below the lower threshold, then it is rejected.
    # If the pixel gradient is between the two thresholds, 
    # then it will be accepted only if it is connected to a pixel that is above the upper threshold.
    # Canny recommended a upper:lower ratio between 2:1 and 3:1.
    img_canny = cv2.Canny(img_blur, threshold_lower, threshold_upper, aperture_size,  L2gradient = L2Gradient )
    # cv2.imshow("image", img_canny)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    # cv2.imshow("canny", img_canny)
    # cv2.waitKey()

    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print("contours1: ", len(contours))
    
    n = 0
    for cnt in contours:
   
        # It is also called arc length. 
        # It can be found out using cv.arcLength() function. 
        # Second argument specify whether shape is a closed contour (if passed True), or just a curve.
        perimeter = cv2.arcLength(cnt,True)
        if perimeter == False:
            contours = contours[:n] + contours[n+1:]
        n += 1

    img_stack = stack_images(0.8,([img_gray],[img_blur],[img_canny]))
    # cv2.imshow("result", img_stack)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # cv2.drawContours(image, contours, -1, (255,0,0), 1)
    # cv2.imshow("image contour", image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # print("contours2: ", len(contours))
    return contours

def setup_contour(image, amount_of_shapes_in_picture):
    model_custom_path = os.path.join(os.getcwd(), 'files', 'image_processing')
    threshold_values = open(model_custom_path +"\\threshold_values.txt", "w")    
    threshold_lower = 30
    threshold_upper = 0

    def check_area_of_contours(contours):
        counter = 0
        for contour in contours:
            area1 = cv2.contourArea(contour)

            if area1 > 35:
                counter += 1
                if counter == amount_of_shapes_in_picture:
                    print("counter: ", counter)
        return counter

    while(1):

        if len( get_contours_from_image(image, threshold_lower, threshold_upper)) != amount_of_shapes_in_picture:
        # if check_area_of_contours(get_contours_from_image(image, threshold_lower, threshold_upper)) != amount_of_shapes_in_picture:
            threshold_lower +=2
            threshold_upper = threshold_lower

            while(1):
                if len( get_contours_from_image(image, threshold_lower, threshold_upper)) != amount_of_shapes_in_picture:
                # if check_area_of_contours(get_contours_from_image(image, threshold_lower, threshold_upper)) != amount_of_shapes_in_picture:
                    threshold_upper +=5
                    if threshold_upper > 300:
                        threshold_upper = threshold_lower
                        break
                else:
                    threshold_values.write(str(threshold_lower) + "\n" + str(threshold_upper)) 
                    threshold_values.close()
                    return threshold_lower, threshold_upper

            if threshold_lower > 300:
                print("Couldn't find propper threshold values. Return threshold lower is 60 and upper is 180.")
                threshold_lower = 60
                threshold_upper = 180
                threshold_values.write(str(threshold_lower) + "\n" + str(threshold_upper))
                threshold_values.close()
                return threshold_lower, threshold_upper
            
        else:
            threshold_values.write(str(threshold_lower) + "\n" + str(threshold_upper))
            threshold_values.close()
            return threshold_lower, threshold_upper

