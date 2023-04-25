import cv2
import image_processing as img_proc
import common.midi_creation as midi_creation
import common.midi_processing as midi_processing
import image_processing_ai as img_proc_ai
import multiprocessing as mp

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    img_path = 'files\image_processing\example_shapes_1.png'
    img = cv2.imread(img_path)

    # img_proc.setup_contour()

    # while(1):
    #     ret, img = cap.read()

    shapes = img_proc.get_contours_from_image(img)      
    print("shapes: ", len(shapes))
    if len(shapes) < 1:  
        cv2.imshow("ai", img_proc_ai.detect_shapes_with_ai(img))
    else: 
        image, list_of_shapes = img_proc_ai.detect_shapes_with_contour(shapes, img)
        cv2.imshow("contour", image)
    
    # print("press any key to continue...")
    # cv2.waitKey()    
    
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    midi_creation.MakeSong(list_of_shapes) 

    process1 = mp.Process(target=midi_processing.drum, args=(list_of_shapes, 0))
    process2 = mp.Process(target=midi_processing.violin, args=(list_of_shapes, 0))
    process3 = mp.Process(target=midi_processing.guitar, args=(list_of_shapes, 0))
    process4 = mp.Process(target=midi_processing.flute, args=(list_of_shapes, 0))
    process5 = mp.Process(target=midi_processing.cello, args=(list_of_shapes, 0))

    if __name__ == "__main__":
        process1.start()
        process2.start()
        process3.start()
        process4.start()
        process5.start()

        process1.join()
        process2.join()
        process3.join()
        process4.join()
        process5.join() 

    midi_processing.audio_rendering()
    cv2.destroyAllWindows()