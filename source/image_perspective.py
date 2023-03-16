"""Image perspective is a library to turn a photo of a trapezium into a rectangle.

*Use the `warp_perspective()` function to get started...*

Works well with .jpg for now

## BUG & TODO
---
- TODO test `get_whiteboard_dimensions` for weird angles
- BUG `get_whiteboard_dimensions` gives the wrong dimensions
- BUG `get_coordinates_transform_points` works different for .png .bmp. ***(JPG is tested)***
- TODO `get_coordinates_transform_points` add support for `cv2`'s camera frames"""

import common.location
import cv2
import numpy
import os
import time

# Based upon the following works:
# https://learnopencv.com/automatic-document-scanner-using-opencv/  


def resize_image_to_fit_screen(image :cv2.Mat) -> cv2.Mat:
    """Grabs the resolution of the **Primary** screen and resizes the image to fit both demotions"""
    screen_size = common.location.get_screensize()
    image_size = common.location.Pos(x=image.shape[1], y=image.shape[0])
    crop_modifier = min(1, min(screen_size.x / image_size.x, screen_size.y / image_size.y)) # [0 - 1], modifier, to scale image so it fits on the screen
    return cv2.resize(image, (int(image_size.x * crop_modifier),int(image_size.y * crop_modifier)))
def get_coordinates_transform_points(image: cv2.Mat, verbosity_level=0) -> list[list[int,int], list[int,int], list[int,int], list[int,int]]:
    """This expensive function checks the image and does multiple checks to find a trapezium that is inside 5px's of the image boarders.
    Use this function to calibrate the positional-transform (moving the camera into the correct perspective)
    
    ## Parameters
    @param image the image to check for rectangle (works with openCV image or TODO:camera_frame)
    @param verbosity_level 0-2 wherein [   nothing(default),   prints info,   opens images for intermediate steps   ]
    @returns list [Top-Left, Top-Right, Bottom-Right, Bottom-Left]. Where each has a list of [x, y] int
    
    ## Limitations
    - This function does not handle it if the rectangle is not within 5px of the image edges.  
    - The whiteboard should be the largest object in view

    ## TODO & BUG
    - TODO works with camera_frame
    - BUG problems with .png
    - BUG problems with .bmp"""
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
    if (verbosity_level > 1): cv2.imshow(f'Contours',cv2.resize(image_contours, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))

    # Sorting the corners and converting them to desired shape.
    corners = sorted(numpy.concatenate(corners).tolist())
    if (verbosity_level > 0): print(f'Corners: {corners}')
    

    # Rearrange the order of the corners to: top-left, top-right, bottom-right, bottom-left
    # A B
    # D C
    rect = numpy.zeros((4, 2), dtype='float32')
    corners_sorted = numpy.array(corners)
    s = corners_sorted.sum(axis=1)
    # Top-left point will have the smallest sum.
    rect[0] = corners_sorted[numpy.argmin(s)]
    # Bottom-right point will have the largest sum.
    rect[2] = corners_sorted[numpy.argmax(s)]
 
    diff = numpy.diff(corners_sorted, axis=1)
    # Top-right point will have the smallest difference.
    rect[1] = corners_sorted[numpy.argmin(diff)]
    # Bottom-left will have the largest difference.
    rect[3] = corners_sorted[numpy.argmax(diff)]
    corners_sorted = rect.astype('int').tolist()
    if (verbosity_level > 0): print(f'Sorted corners: {corners_sorted}')
    
    # Displaying the corners.
    if (verbosity_level > 1): 
        image_corners_sorted = image_contours
        for index, c in enumerate(corners_sorted):
            character = chr(65 + index)
            cv2.putText(image_corners_sorted, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow(f'Contours with sorted corners',cv2.resize(image_corners_sorted, (int(image_scaled_size.x * crop_modifier),int(image_scaled_size.y * crop_modifier))))


    # Return coordinates of corners
    corners_sorted[0][0] = int((corners_sorted[0][0] * image_size.x) / image_scaled_size.x)
    corners_sorted[0][1] = int((corners_sorted[0][1] * image_size.y) / image_scaled_size.y)
    corners_sorted[1][0] = int((corners_sorted[1][0] * image_size.x) / image_scaled_size.x)
    corners_sorted[1][1] = int((corners_sorted[1][1] * image_size.y) / image_scaled_size.y)
    corners_sorted[2][0] = int((corners_sorted[2][0] * image_size.x) / image_scaled_size.x)
    corners_sorted[2][1] = int((corners_sorted[2][1] * image_size.y) / image_scaled_size.y)
    corners_sorted[3][0] = int((corners_sorted[3][0] * image_size.x) / image_scaled_size.x)
    corners_sorted[3][1] = int((corners_sorted[3][1] * image_size.y) / image_scaled_size.y)

    if (verbosity_level > 0): print(f'Corner Top-Left:\t{corners_sorted[0]}\nCorner Top-Right:\t{corners_sorted[1]}\nCorner Bottom-Right:\t{corners_sorted[2]}\nCorner Bottom-Left:\t{corners_sorted[3]}')
    return corners_sorted
def get_whiteboard_dimensions(coordinates_transform_points: list[list[int,int], list[int,int], list[int,int], list[int,int]], accept_image_loss=False, verbosity_level=0) -> list[int,int]:
    """TODO This """
    import math

    top_left, top_right, bottom_right, bottom_left = coordinates_transform_points

    def difference(a, b):
        return max(a,b) - min(a,b)

    # Calculate the width of the board
    dx = difference(top_left[0], top_right[0])
    dy = difference(top_left[1], top_right[1])
    width_top = int(math.sqrt(dx**2 + dy**2))
    dx = difference(bottom_left[0], bottom_right[0])
    dy = difference(bottom_left[1], bottom_right[1])
    width_bottom = int(math.sqrt(dx**2 + dy**2))

    # Calculate the height of the board
    dx3 = difference(top_left[0], bottom_left[0])
    dy3 = difference(top_left[1], bottom_left[1])
    height_left = int(math.sqrt(dx**2 + dy**2))
    dx3 = difference(top_right[0], bottom_right[0])
    dy3 = difference(top_right[1], bottom_right[1])
    height_right = int(math.sqrt(dx**2 + dy**2))


    if (verbosity_level > 0): print(f'Whiteboard size:\n  min:{[min(width_top,width_bottom),min(height_left,height_right)]}\n  max:{[max(width_top,width_bottom),max(height_left,height_right)]}')


    # TODO Fix. solution does not correctly adjust the pixel size
    if accept_image_loss:
        return [min(width_top,width_bottom),min(height_left,height_right)]
    return [max(width_top,width_bottom),max(height_left,height_right)]
def warp_perspective(image: cv2.Mat, verbosity_level=0) -> cv2.Mat:
    """"""
    # Check input
    assert verbosity_level is not int or verbosity_level < 0 or verbosity_level > 2, "verbosity_level out_of_bounds expected an int in range of (0 - 2)"
    assert image is not None, "I got no input at all, check if you got the correct path"

    # Define sizes
    screen_size = common.location.get_screensize()
    image_size = common.location.Pos(x=image.shape[1], y=image.shape[0])
    crop_modifier = min(1, min(screen_size.x / image_size.x, screen_size.y / image_size.y)) # [0 - 1], modifier, to scale image so it fits on the screen

    # Define transform
    transform_points = get_coordinates_transform_points(image=image, verbosity_level=verbosity_level)
    whiteboard_dimensions = get_whiteboard_dimensions(transform_points, accept_image_loss=False, verbosity_level=verbosity_level)

    whiteboard_size = common.location.Pos(x=whiteboard_dimensions[0], y=whiteboard_dimensions[1])
    crop_modifier = min(1, min(screen_size.x / whiteboard_size.x, screen_size.y / whiteboard_size.y)) # [0 - 1], modifier, to scale image so it fits on the screen

    destination_corners = [[0,0],[whiteboard_size.x,0],[whiteboard_size.x,whiteboard_size.y],[0,whiteboard_size.y]]
    homography = cv2.getPerspectiveTransform(numpy.float32(transform_points), numpy.float32(destination_corners))

    output_img = cv2.warpPerspective(image, homography, (whiteboard_size.x,whiteboard_size.y), flags=cv2.INTER_LINEAR)
    cv2.imshow(f'Final transform',cv2.resize(output_img, (int(whiteboard_size.x * crop_modifier),int(whiteboard_size.y * crop_modifier))))









if __name__ == "__main__":
    print ('Running demo image_perspective\nThis demo is about how to find the corners of an transformed rectangle fully automatically.\nDue to its GIRTH it is advised to only do it per user request or as part of a first time setup.')

    # open an image
    absolute_path = os.path.join(os.getcwd(), 'files', 'image_perspective', 'whiteboard.jpg')
    # absolute_path = os.path.join(os.getcwd(), 'files', 'image_perspective', 'paper.jpg')
    # absolute_path = os.path.join(os.getcwd(), 'files', 'image_perspective', 'paper.png') BUG
    print(f'Opening ({absolute_path}) as an image.')
    img = cv2.imread(absolute_path, 1)
    

    # Using another useful function that make the given image fit inside the current screen
    img_size = common.location.Pos(x=img.shape[1], y=img.shape[0])
    cv2.imshow(f'Input of demo ( width:{img_size.x}, height:{img_size.y} )',resize_image_to_fit_screen(img))
    

    # Using the function
    output_img = warp_perspective(image=img, verbosity_level=2)


    # Using another usefull function that make the given image fit inside the current screen
    output_img_size = common.location.Pos(x=output_img.shape[1], y=output_img.shape[0])
    cv2.imshow(f'Output of demo ( width:{output_img_size.x}, height:{output_img_size.y} )',resize_image_to_fit_screen(output_img))
    

    # Wait so we can visually validate
    cv2.waitKey(delay=300000) # 5 minutes max
