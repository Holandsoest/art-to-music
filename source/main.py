import cv2
#print(cv2.__version__)
import image_processing as img_proc
# import common.midi_creation as midi_creation
# import common.midi_processing as midi_processing
#import common.midi_creation as midi_creation
#import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai


#cap = cv2.VideoCapture('nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink',cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture(0)
#img_proc_ai.setup_ai()

if __name__ == "__main__":
    while(1):
        success, img = cap.read()
        image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)
        cv2.imshow("ai", image_ai)

        img_proc.display_list_of_shapes(list_of_shapes)
        # midi_creation.MakeSong(list_of_shapes)
        # midi_processing.AudiRenderPlugin(list_of_shapes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break 
    