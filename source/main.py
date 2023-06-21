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
import time
if __name__ == "__main__":
    while True:
        take_image.set_jetson_busy(busy=True)
        img = take_image.get_image()
        # img_path = os.path.join(os.getcwd(), 'files','image_processing','example_shapes (3).png')
        # img = cv2.imread(img_path)

        image_ai, list_of_shapes = img_proc_ai.detect_shapes_with_ai(img)
        cv2.destroyAllWindows()
        cv2.imshow('AI processing', image_ai)
        cv2.waitKey(1)# Displays the new image immediately
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

        cv2.destroyAllWindows()
        cv2.imshow('Playing audio... Any key continue...', image_ai)
        cv2.waitKey(1)# Displays the new image immediately
        take_image.set_jetson_busy(busy=False)
        key = midi_processing.play_loop(os.path.join(os.getcwd(), 'files', 'audio_generator', 'created_song.mp3'),
                                                    decay= 0.75,
                                                    cutoff=0.05)
        if key == -1: 
            cv2.destroyAllWindows()
            cv2.imshow('Press any key to start... (q to exit)', image_ai)
            key = cv2.waitKey(0)
        if key == ord('q'): break
    cv2.destroyAllWindows()

