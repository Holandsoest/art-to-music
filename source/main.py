# For adding shape recognition. A useful link https://pyimagesearch.com/2016/02/08/opencv-shape-detection/
# Does not use AI so probably faster to process. For simple shapes also a better solution

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
