import cv2
import os
import image_processing_ai as img_proc_ai
import common.image_properties as img_prop
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

    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    n = 0
    for cnt in contours:
        # It is also called arc length. 
        # It can be found out using cv.arcLength() function. 
        # Second argument specify whether shape is a closed contour (if passed True), or just a curve.
        perimeter = cv2.arcLength(cnt,True)
        if perimeter == False:
            contours = contours[:n] + contours[n+1:]
        n += 1

    # img_stack = stack_images(0.8,([img_gray],[img_blur],[img_canny]))
    return contours

def setup_contour(image, amount_of_shapes_in_picture):
    model_custom_path = os.path.join(os.getcwd(), 'files', 'image_processing')
    threshold_values = open(model_custom_path +"\\threshold_values.txt", "w")    
    threshold_lower = 30
    threshold_upper = 0

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

def detect_shapes_via_contour(contours, image):
    """
    This function goes over all contours that have been read with cv2 
    and will detect all the shapes that would have otherwise been marked as a 'circle'.
    - contours: all contours read with cv2.contours

    Returns an image and a list with details of all the shapes on the image.
    """
    # Create shape list_of_shapes
    list_of_shapes = []

    #Get the height, width and channel of the image
    img_height, img_width, channel = image.shape
    img_size = img_height*img_width

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
        
    counter = 0

    for contour in contours:
        counter += 1
        area1 = cv2.contourArea(contour)

        if area1 > 100:
            # Get approx contour of shape
            # Now you can use this function to approximate the shape. 
            # In this, second argument is called epsilon, which is maximum distance from contour to approximated contour. 
            # It is an accuracy parameter. 
            # A wise selection of epsilon is needed to get the correct output.
            epsilon = 0.02*cv2.arcLength(contour,True)
            approx = cv2.approxPolyDP(contour,epsilon,True)

            # minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
            # It will create a rectangle around the shapes
            rect = cv2.minAreaRect(contour)

            box = cv2.boxPoints(rect)
            # x1, y1, x2, y2 = box
            # middle_point_x = (x1+x2)/2
            # middle_point_y = (y1+y2)/2
            # box = np.int0(box)
            # cv2.drawContours(image,[box],0,(0,0,255),1)
            (x, y), (width, height), angle = rect

            shape_size_to_volume = get_volume_from_size(width*height, img_size)
            shape_colorcode_to_bpm = get_bpm_from_color(int(x),int(y),image)
            shape_width_to_duration = get_duration_from_width(width, img_width)
            shape = img_prop.Image("", counter, 0, int(shape_size_to_volume), int(shape_colorcode_to_bpm), int(shape_width_to_duration), 0, box)
            cv2.putText(image, str(counter), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 120, 120), 2)
            cv2.drawContours(image, contour, -1, (0,255,0), 3)

            if len(approx) == 3:
                # Shape is a triangle (Guitar)
                shape.shape = "triangle"
                shape.instrument = "guitar"
                shape.pitch = int(get_pitch_from_size(height, img_height, "guitar"))

            elif len(approx) == 4 : 
                # x2, y2 , w, h = cv2.boundingRect(approx)
                # aspect_ratio = float(w)/h
                # if aspect_ratio >= 0.95 and aspect_ratio < 1.05:
                shape.shape = "square"
                shape.instrument = "drum"
                shape.pitch = int(get_pitch_from_size(height, img_height, "drum"))
                # Shape is a square (Drum Pads)
                # else:
                #     shape.shape = "square" #actually rectangle
                #     shape.instrument = "drum"
                #     shape.pitch = int(get_pitch_from_size(height, img_height, "drum"))
                #     # Shape is a rectangle (Drum Pads)

            elif len(approx) == 10 :
                # Shape is a star (Cello)
                shape.shape = "star"
                shape.instrument = "cello"
                shape.pitch = int(get_pitch_from_size(height, img_height, "cello"))
            else:
                # Shape is half circle, circle or heart
                # Use AI to detect other shapes
                shape_name = img_proc_ai.detect_shape_with_ai(get_image_from_box(contour, image))
                if shape_name == "empty":
                    shape.pitch = int(get_pitch_from_size(height, img_height, "empty"))
                    continue

                else: 
                    shape.shape = shape_name
                    if shape_name == "half circle":
                        shape_name = "flute"
                    elif shape_name == "heart": 
                        shape_name = "piano"
                    elif shape_name == "circle":
                        shape_name = "violin"
                    elif shape_name == "square":
                        shape_name = "drum"
                    elif shape_name == "triangle":
                        shape_name = "guitar"
                    elif shape_name == "star":
                        shape_name = "cello"
                    shape.instrument = shape_name
                    shape.pitch = int(get_pitch_from_size(height, img_height, shape_name))

            list_of_shapes.append(shape)
            # cv2.putText(image, shape.shape, (x[0],y[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.putText(image, str(counter), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 120, 120), 2)
            
        else:
            continue
    
    # TODO: Sort list_of_shapes in this order:
    # "circle", "half circle", "square", "heart", "star", "triangle"
    # def sort_func(list_item):
    #     return len(list_item)

    # list_of_shapes.sort(key=sort_func)

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

def compare_list_of_shapes_contour_with_ai(list_of_shapes_contour, list_of_shapes_ai):
    list_of_shapes_combined = []
    # list_of_shapes_combined1 = []
    # list_of_shapes_contour_copy = list_of_shapes_contour.copy()
    # list_of_shapes_ai_copy = list_of_shapes_ai.copy()

    for shape_contour in list_of_shapes_contour:
        middle_x, middle_y = shape_contour.middlepoint
        for shape_ai in list_of_shapes_ai:
            x1, y1, x2, y2 = shape_ai.box
            if ((x1 <= middle_x[0] <= x2) and (y1 <= middle_y[1] <= y2)):
                #   Point is in bounding box
                list_of_shapes_combined.append(shape_ai)
                list_of_shapes_ai.remove(shape_ai)

    # for shape_ai1 in list_of_shapes_ai_copy:
    #     middle_x, middle_y = shape_ai1.middlepoint
    #     for shape_contour1 in list_of_shapes_contour_copy:
    #         x1, y1, x2, y2 = shape_contour1.box
    #         if ((x1 <= middle_x[0] <= x2) and (y1 <= middle_y[1] <= y2)):
    #             #   Point is in bounding box
    #             list_of_shapes_combined1.append(shape_ai)
    #             list_of_shapes_contour.remove(shape_contour1)
    
    # for shape in list_of_shapes_combined1:
    #     print(shape.counter, 
    #           "shape:", shape.shape, 
    #           "instrument:", shape.instrument, 
    #           "volume:", shape.volume, 
    #           "bpm:", shape.bpm, 
    #           "pitch:", shape.pitch, 
    #           "duration:", shape.duration, 
    #           sep='\t')
        
    # print("---------------------------------------------------------------------")

    for shape in list_of_shapes_combined:
        print(shape.counter, 
              "shape:", shape.shape, 
              "instrument:", shape.instrument, 
              "volume:", shape.volume, 
              "bpm:", shape.bpm, 
              "pitch:", shape.pitch, 
              "duration:", shape.duration, 
              sep='\t')
    
    return list_of_shapes_combined