import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai

cap = cv2.VideoCapture(0)
img_proc_ai.setup_ai()

if __name__ == "__main__":
    img_counter = 0
    img_path = 'files\image_processing\opencv_fram_5.png'
    img = cv2.imread(img_path)
    assert img is not None, "file could not be read, check with os.path.exists()"

    image_ai, list_of_shapes_ai = img_proc_ai.detect_shapes_with_ai(img)
    cv2.imshow("result", img)
    cv2.waitKey()

    # while(1):
    #     success, img = cap.read()

    #     cv2.imshow("Result", img)

    #     if cv2.waitKey(1) & 0xFF == ord('w'):
    #         print("Getting list of shapes... Please wait...")
    #         img_path = "opencv_fram_{}.png".format(img_counter)
    #         cv2.imwrite(img_path, img)
    #         print("screenshot taken")
    #         img_path = "opencv_fram_{}.png".format(img_counter)
    #         img = cv2.imread(img_path)
    #         img_counter+=1 

    #         image_ai, list_of_shapes_ai = img_proc_ai.detect_shapes_with_ai(img)
    #         cv2.imshow("ai", image_ai)
    #     elif cv2.waitKey(1) & 0xFF == ord('q'):
    #         break 

    print("All shapes are detected, enjoy the music")
    img_proc.display_list_of_shapes(list_of_shapes_ai)
    # midi_creation.MakeSong(list_of_shapes)
    # midi_processing.AudiRenderPlugin(list_of_shapes)
    cv2.destroyAllWindows()