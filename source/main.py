import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    img_path = 'files\image_processing\Voorbeeld_camera_licht.jpg'
    # img_path = 'files\image_processing\example_shapes (5).jpg'
    img_path = 'files\image_processing\example_shapes.png'
    img = cv2.imread(img_path)
    assert img is not None, "file could not be read, check with os.path.exists()"

    amount_of_shapes_in_picture = 16
    threshold_lower, threshold_upper = img_proc.setup_contour(img, amount_of_shapes_in_picture)
    print ("threshold lower: ", threshold_lower)
    print ("threshold upper: ", threshold_upper)

    shapes = img_proc.get_contours_from_image(img, threshold_lower, threshold_upper)
    print("shapes: ", len(shapes))

    if len(shapes) < 1:  
        image = cv2.imread(img_proc_ai.detect_shapes_with_ai(img))
    else: 
        image, list_of_shapes = img_proc_ai.detect_shapes_with_contour(shapes, img)

    cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE) 
    image = cv2.resize(image, (960, 540)) 
    cv2.imshow("output", image)

    if len(list_of_shapes) != amount_of_shapes_in_picture:
        print("Setup failed! ", amount_of_shapes_in_picture - len(list_of_shapes) , " shapes are not recognized :(")
            
    else:
        print("All shapes are detected, enjoy the music")
        cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE) 
        image = cv2.resize(image, (960, 540)) 
        cv2.imshow("output", image)
        midi_creation.MakeSong(list_of_shapes)
        midi_processing.AudiRenderPlugin(list_of_shapes)
            

    print("press any button to continue...")
    cv2.waitKey()
    cv2.destroyAllWindows()

    # cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE) 
    # image = cv2.resize(image, (960, 540)) 
    # cv2.imshow("output", image)
    # print("press any button to continue...")
    # cv2.waitKey()