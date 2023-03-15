import common.location
import cv2
import numpy
import os
import time

res_image_processing = common.location.Pos(x=1920, y=1080)

# Based upon the following works:
# https://learnopencv.com/automatic-document-scanner-using-opencv/  

def get_coordinates_transform_points(image, verbosity_level=0):
    """This expensive function checks the image and does multiple checks to find a trapezium that is inside 5px's of the image boarders.
    Use this function to calibrate the positional-transform (moving the camera into the correct perspective)
    
    ## Parameters
    @param image the image to check for rectangle (works with openCV image or TODO:camera_frame)
    @param verbosity_level 0-2 wherein [   nothing(default),   prints info,   opens images for intermediate steps   ]
    TODO: @returns tuple with 4 common.location.Pos in the order TopLeft,TopRight,BottomLeft,BottomRight
    
    ## Limitations
    - This function does not handle it well if the rectangle is not within 5px of the image edges.  
    - This function does not handle it well if the rectangle is not within 5px of the image edges.  

    ## TODO & BUG
    - TODO works with camera_frame
    - TODO work out interface
    - BUG problems with .png
    - BUG problems with .bmp
    """
    # Check input
    assert verbosity_level is not int or verbosity_level < 0 or verbosity_level > 2, "verbosity_level out_of_bounds expected an int in range of (0 - 2)"
    assert image is not None, "I got no input at all, check if you got the correct path"


    # Define sizes
    max_processing_size = common.location.Pos(x=1920, y=1080)
    screen_size = common.location.get_screensize()
    image_size = common.location.Pos(x=image.shape[1], y=image.shape[0])
    crop_modifier = min(1, min(screen_size.x / image_size.x, screen_size.y / image_size.y)) # [0 - 1], modifier, to scale image so it fits on the screen
    if (verbosity_level > 0): print(f'Sizes:\n  Primary screen size:\t{screen_size}\n  Original image:\t{image_size}\n  Cropped image:\tx:{int(image_size.x*crop_modifier)}, y:{int (image_size.y*crop_modifier)}, modifier:{crop_modifier}')
    if (verbosity_level > 1): cv2.imshow(f'Before image',cv2.resize(image, (int(image_size.x * crop_modifier),int(image_size.y * crop_modifier))))


    # Remove foreground
    kernel = numpy.ones((3,3),numpy.uint8)
    image_morphed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations= 10)
    if (verbosity_level > 1): cv2.imshow(f'After Morphing',cv2.resize(image_morphed, (int(image_size.x * crop_modifier),int(image_size.y * crop_modifier))))


    # Crop the image down so it can be processed
    crop_modifier = min(1, min(max_processing_size.x / image_size.x, max_processing_size.y / image_size.y)) # [0 - 1], modifier, to scale the image so it can be processed
    image_scaled_size = common.location.Pos(x=int(image_size.x * crop_modifier), y=int(image_size.y * crop_modifier))
    image_scaled = cv2.resize(image_morphed, (image_scaled_size.x, image_scaled_size.y))
    crop_modifier = min(1, min(screen_size.x / image_scaled_size.x, screen_size.y / image_scaled_size.y)) # [0 - 1], modifier, to scale image so it fits on the screen
    if (verbosity_level > 0): print(f'  After scaling:\tx:{image_scaled_size.x}, y:{image_scaled_size.y}, modifier:{crop_modifier}')
    if (verbosity_level > 1): cv2.imshow(f'After Scaling',cv2.resize(image_scaled, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))


    # GrabCut (remove the background)
    mask = numpy.zeros(image_scaled.shape[:2],numpy.uint8)
    bgdModel = numpy.zeros((1,65),numpy.float64)
    fgdModel = numpy.zeros((1,65),numpy.float64)
    rect = (5, 5, image_scaled_size.x-10, image_scaled_size.y-10)
    image_grabcut = image_scaled
    cv2.grabCut(image_grabcut, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
    mask2 = numpy.where((mask==2)|(mask==0),0,1).astype('uint8')
    image_grabcut = image_grabcut * mask2[:,:,numpy.newaxis]
    if (verbosity_level > 1): cv2.imshow(f'After GrabCut',cv2.resize(image_grabcut, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))


    # Blur
    image_gray = cv2.cvtColor(image_grabcut, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.GaussianBlur(image_gray, (11, 11), 0)
    if (verbosity_level > 1): cv2.imshow(f'After Grayscale and Blur',cv2.resize(image_gray, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))
    

    # Edge Detection.
    image_edge = cv2.Canny(image_gray, 0, 140)
    image_edge = cv2.dilate(image_edge, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    if (verbosity_level > 1): cv2.imshow(f'After Canny',cv2.resize(image_edge, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))


    # Detect contours and only keep the largest one
    image_contours = numpy.zeros_like(image_scaled)

    # Finding contours for the detected edges.
    contours, hierarchy = cv2.findContours(image_edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Keeping only the largest detected contour.
    whiteboard = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    image_contours = cv2.drawContours(image_contours, whiteboard, -1, (0, 255, 255), 3)

    # Loop over the contours.
    for c in whiteboard:
        # Approximate the contour.
        epsilon = 0.02 * cv2.arcLength(c, True)
        corners = cv2.approxPolyDP(c, epsilon, True)
        # If our approximated contour has four points
        if len(corners) == 4:
            break
    cv2.drawContours(image_contours, c, -1, (0, 255, 255), 3)
    cv2.drawContours(image_contours, corners, -1, (0, 255, 0), 10)

    # Sorting the corners and converting them to desired shape.
    corners = sorted(numpy.concatenate(corners).tolist())
    if (verbosity_level > 0): print(f'Corners: {corners}')
    
    # Displaying the corners.
    if (verbosity_level > 1): 
        for index, c in enumerate(corners):
            character = chr(65 + index)
            cv2.putText(image_contours, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow(f'Contours2',cv2.resize(image_contours, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))
    




    # raise NotImplementedError # NOTE: This is a placeholder
    return (common.location.Pos(),common.location.Pos(),common.location.Pos(),common.location.Pos())









if __name__ == "__main__":
    print ('Running demo image_perspective\nThis demo is about how to find the corners of an transformed rectangle fully automatically.\nDue to its GIRTH it is advised to only do it per user request or as part of a first time setup.')

    # 'Generate' an image
    absolute_path = os.path.join(os.getcwd(), 'source', 'haw.jpg')
    # absolute_path = os.path.join(os.getcwd(), 'source', '20230314_100721.jpg')
    # absolute_path = os.path.join(os.getcwd(), 'source', '20230314_100721.png')
    # absolute_path = os.path.join(os.getcwd(), 'source', 'Trapesium.bmp')
    print(f'Opening ({absolute_path}) as an image.')
    img = cv2.imread(absolute_path, 1)

    # Find the whiteboard coordinates
    get_coordinates_transform_points(image=img, verbosity_level=2)

    # def order_points(pts):
    #     '''Rearrange coordinates to order:
    #     top-left, top-right, bottom-right, bottom-left'''
    #     rect = numpy.zeros((4, 2), dtype='float32')
    #     pts = numpy.array(pts)
    #     s = pts.sum(axis=1)
    #     # Top-left point will have the smallest sum.
    #     rect[0] = pts[numpy.argmin(s)]
    #     # Bottom-right point will have the largest sum.
    #     rect[2] = pts[numpy.argmax(s)]
    
    #     diff = numpy.diff(pts, axis=1)
    #     # Top-right point will have the smallest difference.
    #     rect[1] = pts[numpy.argmin(diff)]
    #     # Bottom-left will have the largest difference.
    #     rect[3] = pts[numpy.argmax(diff)]
    #     # Return the ordered coordinates.
    #     return rect.astype('int').tolist()
    # def find_dest(pts):
    #     (tl, tr, br, bl) = pts
    #     # Finding the maximum width.
    #     widthA = numpy.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    #     widthB = numpy.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    #     maxWidth = max(int(widthA), int(widthB))
    
    #     # Finding the maximum height.
    #     heightA = numpy.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    #     heightB = numpy.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    #     maxHeight = max(int(heightA), int(heightB))
    #     # Final destination co-ordinates.
    #     destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]
    #     return order_points(destination_corners)
    # destination_coordinates_points = find_dest(corners)
    # print(destination_coordinates_points)


    # Wait so we can visually validate
    cv2.waitKey(delay=300000) # 5 minutes
