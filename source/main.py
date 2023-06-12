import cv2
import numpy as np
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import image_processing as img_proc
import take_image
import multiprocessing as mp

img_proc_ai.setup_ai()

import os

if __name__ == "__main__":
    # TODO: Do this when jetson button press
    
    img = take_image.get_image()
    cv2.imshow('Camera', img)

    image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)
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

    # TODO: play audio with pygame

    cv2.waitKey(0)
    cv2.destroyAllWindows()

