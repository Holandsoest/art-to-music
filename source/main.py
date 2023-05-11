import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import numpy as np

cap = cv2.VideoCapture(0)
img_proc_ai.setup_ai()

if __name__ == "__main__":
    img_counter = 0
    # img_path = 'files\image_processing\example_shapes (7).jpg'
    # img_path = 'files\image_processing\Voorbeeld_camera_licht_cropped.jpg'
    img_path = 'files\image_processing\example_shapes_1.png' #15
    img = cv2.imread(img_path)
    img_copy = img.copy()
    assert img is not None, "file could not be read, check with os.path.exists()"

    do_setup = False
    if do_setup == False:
        threshold_handle = open('files\\image_processing\\threshold_values.txt', 'r')
        list_threshold = threshold_handle.readlines()
        threshold_lower = int(list_threshold[0])
        threshold_upper = int(list_threshold[1])
        threshold_handle.close()
    else:
        amount_of_shapes_in_picture = 15
        # success, img = cap.read()
        threshold_lower, threshold_upper = img_proc.setup_contour(img, amount_of_shapes_in_picture)

    # print ("threshold lower: ", threshold_lower)
    # print ("threshold upper: ", threshold_upper)

    # contours = img_proc.get_contours_from_image(img, threshold_lower, threshold_upper)
    # image_ai, list_of_shapes_ai = img_proc_ai.detect_shapes_with_ai(img)
    # image_contour, list_of_shapes_contour = img_proc.detect_shapes_via_contour(contours, img_copy)

    while(1):
        success, img = cap.read()

        cv2.imshow("Result", img)

        if cv2.waitKey(1) & 0xFF == ord('w'):
            img_path = "opencv_fram_{}.png".format(img_counter)
            cv2.imwrite(img_path, img)
            print("screenshot taken")
            img_path = "opencv_fram_{}.png".format(img_counter)
            img = cv2.imread(img_path)
            img_copy = img.copy()
            img_counter+=1 

            contours = img_proc.get_contours_from_image(img, threshold_lower, threshold_upper)
            image_ai, list_of_shapes_ai = img_proc_ai.detect_shapes_with_ai(img)
            image_contour, list_of_shapes_contour = img_proc.detect_shapes_via_contour(contours, img_copy)
            cv2.imshow("ai", image_ai)
            
            cv2.imshow("contour", image_contour)

        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break 

    print("All shapes are detected, enjoy the music")
    img_proc.compare_list_of_shapes_contour_with_ai(list_of_shapes_contour, list_of_shapes_ai)
    # midi_creation.MakeSong(list_of_shapes)
    # midi_processing.AudiRenderPlugin(list_of_shapes)
    cv2.destroyAllWindows()