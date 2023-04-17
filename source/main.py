import cv2
import image_processing as img_proc
import common.midi_creation as mc
import image_processing_ai as img_proc_ai

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    img_path = 'files\image_processing\example_shapes_1.png'
    img = cv2.imread(img_path)

    # img_proc.setup_contour()

    # while(1):
    #     ret, img = cap.read()

    shapes = img_proc.get_contours_from_image(img)      
    print("shapes: ", len(shapes))
    if len(shapes) < 1:  
        cv2.imshow("ai", img_proc_ai.detect_shapes_with_ai(img))
    else: 
        cv2.imshow("contour", img_proc_ai.detect_shapes_with_contour(shapes, img))
    
    cv2.waitKey()    
    
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    mc.MakeSong(list_of_shapes)