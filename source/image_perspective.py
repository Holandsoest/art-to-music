import common.location
import cv2
import numpy
import os

if __name__ == "__main__":
    print ('Running demo image_perspective\nThis demo is about how to find the corners of an transformed rectangle fully automaticly.\nDue to its GIRTH it is adviced to only do it per user request or as part of a first time setup.')

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

    # Find the whiteboard coordinates

    # Repeated Closing operation to remove text from the document. (remove foreground)
    kernel = numpy.ones((5,5),numpy.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations= 15)
    cv2.imshow(f'After Morphing',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Grabcut (remove the background)
    mask = numpy.zeros(img.shape[:2],numpy.uint8)
    bgdModel = numpy.zeros((1,65),numpy.float64)
    fgdModel = numpy.zeros((1,65),numpy.float64)
    rect = (20,20,img.shape[1]-20,img.shape[0]-20)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = numpy.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,numpy.newaxis]
    cv2.imshow(f'After Grabcut',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Blur
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (11, 11), 0)
    cv2.imshow(f'After Blur',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))
    
    # Edge Detection.
    img = cv2.Canny(img, 0, 100)
    img = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    cv2.imshow(f'After Canny',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Blank canvas.
    con = numpy.zeros_like(img)
    # Finding contours for the detected edges.
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # Keeping only the largest detected contour.
    page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    con = cv2.drawContours(con, page, -1, (0, 255, 255), 3)
    cv2.imshow(f'Contours',cv2.resize(con, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))



    # Wait so we can visually validate
    cv2.waitKey(delay=300000) # 5 minutes
