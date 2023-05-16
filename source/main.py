import cv2
import image_processing as img_proc
#import common.midi_creation as midi_creation
#import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai

#cap = cv2.VideoCapture(0)
img_proc_ai.setup_ai()

if __name__ == "__main__":
    while(1):
        #change
        img_counter = 0
        img_path = 'files\\image_processing\\test_shapes_with_camera0.png'
        img_path = 'files\image_processing\opencv_fram_5.png'
        img = cv2.imread(img_path)
        assert img is not None, "file could not be read, check with os.path.exists()"
        image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)
        cv2.imshow("ai", image_ai)

        img_proc.display_list_of_shapes(list_of_shapes)
        # midi_creation.MakeSong(list_of_shapes)
        # midi_processing.AudiRenderPlugin(list_of_shapes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break 
    