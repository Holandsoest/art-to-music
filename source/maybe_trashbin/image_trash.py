# part of the image_perspective.py
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

