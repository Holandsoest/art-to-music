import cv2
import image_processing as img_proc
import common.midi_creation as mc

if __name__ == "__main__":
    img = cv2.imread('files\image_processing\ExampleShapes6.png')

    list_of_shapes = img_proc.readImage(img)

    print('Press esc to continue...')   

    while(1):
        cv2.imshow("image",img)

        #Break the loop when user hits 'esc' key 
        if cv2.waitKey(20) & 0xFF ==27:
            print('Enjoy the music')
            break
        
    mc.MakeSong(list_of_shapes)     
    cv2.destroyAllWindows()

