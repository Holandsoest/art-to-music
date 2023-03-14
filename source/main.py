import image_perspective
import cv2
import numpy
import common.location
import os
import time

if __name__ == "__main__":

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
    # cv2.imshow(f'Before',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Find the whiteboard coordinates
    crop_modifier = common.location.Pos(x=(image_perspective.res_image_processing.x / img_size.x), y=(image_perspective.res_image_processing.y / img_size.y))
    img = cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min())))

    # Repeated Closing operation to remove text from the document. (remove foreground)
    kernel = numpy.ones((3,3),numpy.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations= 5)
    cv2.imshow(f'After Morphing',img)

    image_perspective.anti_outline_edge_collision_grabcut(image=img)

    # Wait so we can visually validate
    cv2.waitKey(delay=300000) # 5 minutes
