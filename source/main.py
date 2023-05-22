import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import multiprocessing as mp

cap = cv2.VideoCapture(0)
img_proc_ai.setup_ai()

import os

if __name__ == "__main__":
    absolute_img_path = os.path.join(os.getcwd(), 'files','image_processing','example_shapes ().png')
    img = cv2.imread(absolute_img_path)
    assert img is not None, "file could not be read, check with os.path.exists()"

    # while(1):
        # success, img = cap.read()
    image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)

    img_proc_ai.detect_shapes_with_ai(img)
    img_proc.display_list_of_shapes(list_of_shapes)

    midi_creation.MakeSong(list_of_shapes) 
    
    processes = [
        mp.Process(target=midi_processing.drum, args=(list_of_shapes, 0)),
        mp.Process(target=midi_processing.violin, args=(list_of_shapes, 0)),
        mp.Process(target=midi_processing.guitar, args=(list_of_shapes, 0)),
        mp.Process(target=midi_processing.flute, args=(list_of_shapes, 0)),
        mp.Process(target=midi_processing.saxophone, args=(list_of_shapes, 0)),
        mp.Process(target=midi_processing.clap, args=(list_of_shapes, 0)),
        mp.Process(target=midi_processing.piano, args=(list_of_shapes, 0))
    ]
    
    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()
        
    midi_processing.audio_rendering()
    
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break 
    
