import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai

# cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    img_path = 'files\image_processing\example_shapes (7).jpg'
    # img_path = 'files\image_processing\Voorbeeld_camera_schaduw.jpg'
    img = cv2.imread(img_path)
    assert img is not None, "file could not be read, check with os.path.exists()"

    do_setup = True
    if do_setup == False:
        threshold_handle = open('files\\image_processing\\threshold_values.txt', 'r')
        list_threshold = threshold_handle.readlines()
        threshold_lower = int(list_threshold[0])
        threshold_upper = int(list_threshold[1])
        threshold_handle.close()
    else:
        amount_of_shapes_in_picture = 49
        threshold_lower, threshold_upper = img_proc.setup_contour(img, amount_of_shapes_in_picture)
        
    print ("threshold lower: ", threshold_lower)
    print ("threshold upper: ", threshold_upper)

    shapes = img_proc.get_contours_from_image(img, threshold_lower, threshold_upper)
    print("shapes: ", len(shapes))

    if len(shapes) < 1:
        image = cv2.imread(img_proc_ai.detect_shapes_with_ai(img))
    else: 
        image, list_of_shapes = img_proc_ai.detect_shapes_with_contour(shapes, img)

    print("All shapes are detected, enjoy the music")
    cv2.namedWindow("output", cv2.WINDOW_AUTOSIZE) 
    cv2.imshow("output", image)
    # midi_creation.MakeSong(list_of_shapes)
    # midi_processing.AudiRenderPlugin(list_of_shapes)
            
    print("Press any button to continue...")
    cv2.waitKey()
    cv2.destroyAllWindows()