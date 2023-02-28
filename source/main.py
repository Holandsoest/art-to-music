#Follow this guide: https://imageai.readthedocs.io/en/latest/ 
#This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
# This code contains code for activating webcam. Everything commented out is code for object class detection
#Yet to be added processing for the color, the object size size..

import cv2

if __name__ == "__main__":


	#Set webcam parametres
	cam_feed = cv2.VideoCapture(0) 
	cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
	cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)
    #Run Camera in the loop

	while True:
		ret, frame = cam_feed.read()   
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cam_feed.release()
	cv2.destroyAllWindows()
