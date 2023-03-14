import common.location
import cv2
import numpy
import os
import time

res_image_processing = common.location.Pos(x=1920, y=1080)

# Based upon the following works:
# https://learnopencv.com/automatic-document-scanner-using-opencv/  

def get_coordinates_transform_points(image, verbosity_level=0) -> tuple():
    """NOTE DESCRIPTION TBA"""
    # Check input
    assert verbosity_level is not int or verbosity_level < 0 or verbosity_level > 3, "verbosity_level out_of_bounds expected an int in range of (0 - 3)"
    assert image is not None, "I got no input at all, check if you got the correct path"
    raise NotImplementedError # NOTE: This is a placeholder
    return (common.location.Pos(),common.location.Pos(),common.location.Pos(),common.location.Pos())

def anti_outline_edge_collision_grabcut(image):

    def grabcut_rectangle(image, rect):
        """Cuts the image according to rectangle"""
        mask = numpy.zeros(image.shape[:2],numpy.uint8)
        bgdModel = numpy.zeros((1,65),numpy.float64)
        fgdModel = numpy.zeros((1,65),numpy.float64)
        cv2.grabCut(image,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
        mask2 = numpy.where((mask==2)|(mask==0),0,1).astype('uint8')
        image = image*mask2[:,:,numpy.newaxis]
        return image
    
    top = right = bottom = left = iter = 0
    intersection = {
        "north": True,
        "east": True,
        "south": True,
        "west": True
    }
    if any(intersection):
        if intersection['north']:
            top = top + 5
        if intersection['east']:
            right = right + 5
        if intersection['south']:
            bottom = bottom + 10
        if intersection['west']:
            left = left + 10
        
        # Perform GrabCut on image
        rect = (right,top,image.shape[1]-left,image.shape[0]-bottom)
        image = grabcut_rectangle(image=image, rect=rect)

        # Get edges of image
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (11, 11), 0)
        img_canny = cv2.Canny(img_blur, 0, 140)

        # Detect edges intersection with boarder

        # Display verbose output
        iter = iter + 1
        print(f'After Grabcut:{iter} | rect:{rect}')
        print(f'Intersections:{intersection}\n')
        cv2.imshow(f'After Grabcut {iter}',image)
        cv2.imshow(f'After Canny {iter}',img_canny)

        if image.shape[0] - right < 10 or image.shape[1] - bottom < 10:
            raise "Could not find a grabCut that satisfied. I ran out of image."








if __name__ == "__main__":
    print ('Running demo image_perspective\nThis demo is about how to find the corners of an transformed rectangle fully automatically.\nDue to its GIRTH it is advised to only do it per user request or as part of a first time setup.')

    # 'Generate' an image
    absolute_path = os.path.join(os.getcwd(), 'source', 'haw.jpg')
    print(f'Opening ({absolute_path}) as an image.')
    img = cv2.imread(absolute_path, 1)

    # Get the sizes and crop the image if necessary
    assert img is not None, "image is not given, check if os.path.exists()"
    screen_size = common.location.get_screensize()
    img_size = common.location.Pos(x=img.shape[1], y=img.shape[0])
    crop_modifier = common.location.Pos(x=(screen_size.x / img_size.x), y=(screen_size.y / img_size.y))
    print(f'Sizes:\n  Screen:\t{screen_size}\n  Original img:\t{img_size}')
    print(f'  Cropped img:\tx:{int(img_size.x*crop_modifier.min())}, y:{int (img_size.y*crop_modifier.min())}, modifier:{crop_modifier.min()}')
    cv2.imshow(f'Before',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Repeated Closing operation to remove text from the document. (remove foreground)
    kernel = numpy.ones((3,3),numpy.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations= 10)
    cv2.imshow(f'After Morphing',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Find the whiteboard coordinates
    crop_modifier = common.location.Pos(x=(res_image_processing.x / img_size.x), y=(res_image_processing.y / img_size.y))
    img = cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min())))

    # GrabCut (remove the background)
    mask = numpy.zeros(img.shape[:2],numpy.uint8)
    bgdModel = numpy.zeros((1,65),numpy.float64)
    fgdModel = numpy.zeros((1,65),numpy.float64)
    rect = (5,5,img.shape[1]-10,img.shape[0]-10)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,10,cv2.GC_INIT_WITH_RECT)
    mask2 = numpy.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,numpy.newaxis]
    cv2.imshow(f'After Grabcut TopLeft',img)

    # Blur
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (11, 11), 0)
    # cv2.imshow(f'After Blur',img)
    
    # Edge Detection.
    img = cv2.Canny(img, 0, 140)
    img = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cv2.imshow(f'After Canny',img)

    # Blank canvas.
    con = numpy.zeros_like(img)
    # Finding contours for the detected edges.
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Keeping only the largest detected contour.
    page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    con = cv2.drawContours(con, page, -1, (0, 255, 255), 3)
    # cv2.imshow(f'Contours',img)



    # Wait so we can visually validate
    cv2.waitKey(delay=300000) # 5 minutes
