import cv2
import image_processing as img_proc
import common.midi_creation as mc
import image_processing_ai as img_proc_ai

if __name__ == "__main__":
    img_path = 'files\image_processing\example_shapes (14).png'
    img = cv2.imread(img_path)

    # list_of_shapes, shapes = img_proc.readImage(img)
    shapes = img_proc.get_contour_from_image(img)

    img_proc_ai.detect_shapes_with_contour(shapes, img)

    print('Press esc to continue...')   

    while(1):
        cv2.imshow("image",img)

        #Break the loop when user hits 'esc' key 
        if cv2.waitKey(20) & 0xFF ==27:
            print('Enjoy the music')
            break
        
    cv2.destroyAllWindows()

    # mc.MakeSong(list_of_shapes)