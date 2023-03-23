import cv2
import image_processing as img_proc
import common.midi_creation as mc
import image_processing_ai as img_proc_ai

if __name__ == "__main__":
    img = cv2.imread('files\image_processing\ExampleShapes3.png')

    # list_of_shapes = img_proc.readImage(img)

    img_proc_ai.detect_shapes(img)

    # print('Press esc to continue...')   

    # while(1):
    #     cv2.imshow("image",img)

    #     #Break the loop when user hits 'esc' key 
    #     if cv2.waitKey(20) & 0xFF ==27:
    #         print('Enjoy the music')
    #         break
        
    cv2.destroyAllWindows()

    # mc.MakeSong(list_of_shapes)