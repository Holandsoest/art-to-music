import common.location
import cv2
import os

if __name__ == "__main__":
    print ('Running demo image_perspective')
    absolute_path = os.path.join(os.getcwd(), 'source', 'haw.jpg')
    print(absolute_path)
    img = cv2.imread(absolute_path, 1)

    # Get the sizes and crop the image if necessary
    screen_size = common.location.get_screensize()
    img_size = common.location.Pos(x=img.shape[1], y=img.shape[0])
    crop_modifier = common.location.Pos(x=(screen_size.x / img_size.x), y=(screen_size.y / img_size.y))
    print(f'Sizes:\n  Screen:\t{screen_size}\n  Original img:\t{img_size}')
    print(f'  Cropped img:\tx:{int(img_size.x*crop_modifier.min())}, y:{int(img_size.y*crop_modifier.min())}, modifier:{crop_modifier.min()}')
    cv2.imshow(f'Before',cv2.resize(img, (int(img_size.x * crop_modifier.min()),int(img_size.y * crop_modifier.min()))))

    # Find the whiteboard coordinates
    

    cv2.waitKey(delay=0)
