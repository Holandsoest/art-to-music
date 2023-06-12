import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import multiprocessing as mp

cap = cv2.VideoCapture(0)
img_proc_ai.setup_ai()

if __name__ == "__main__":
    img_path = 'files\image_processing\example_shapes (2).png'
    img = cv2.imread(img_path)
    assert img is not None, "file could not be read, check with os.path.exists()"

    # while(1):
        # success, img = cap.read()
    image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)

    img_proc_ai.detect_shapes_with_ai(img)
    img_proc.display_list_of_shapes(list_of_shapes)

    bpm = midi_creation.MakeSong(list_of_shapes) 
    
    processes = [
        mp.Process(target=midi_processing.instrument, args=(bpm, "drum")),
        mp.Process(target=midi_processing.instrument, args=(bpm, "violin")),
        mp.Process(target=midi_processing.instrument, args=(bpm, "guitar")),
        mp.Process(target=midi_processing.instrument, args=(bpm, "flute")),
        mp.Process(target=midi_processing.instrument, args=(bpm, "saxophone")),
        mp.Process(target=midi_processing.instrument, args=(bpm, "clap")),
        mp.Process(target=midi_processing.instrument, args=(bpm, "piano"))
    ]
    
    # Start all processes
    for process in processes:
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()
        
    midi_processing.audio_rendering(bpm)
    
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break 
    
