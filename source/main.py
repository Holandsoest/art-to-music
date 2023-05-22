import cv2
import image_processing as img_proc
import common.midi_creation as mc

import os

if __name__ == "__main__":
    absolute_path = os.path.join(os.getcwd(), 'files','image_processing','ExampleShapes6.png')
    img = cv2.imread(absolute_path)

    list_of_shapes = img_proc.readImage(img)

    print('Press esc to continue...')   

    while(1):
        cv2.imshow("image",img)

        #Break the loop when user hits 'esc' key 
        if cv2.waitKey(20) & 0xFF ==27:
            print('Enjoy the music')
            break
        
    cv2.destroyAllWindows()

    mc.MakeSong(list_of_shapes)