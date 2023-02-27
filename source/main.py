#Follow this guide: https://imageai.readthedocs.io/en/latest/ 
#This is for processing while using webcam https://wellsr.com/python/object-detection-from-webcams-with-yolo/
# This code contains code for activating webcam. Everything commented out is code for object class detection
#Yet to be added processing for the color, the object size size..

#from imageai.Detection import ObjectDetection # For AI object detection AI
import cv2

if __name__ == "__main__":
	
	#----------- AI OBJECT DETECTION --------------------
#obj_detect = ObjectDetection()
#obj_detect.setModelTypeAsYOLOv3()
#obj_detect.setModelPath(r"C:\Users\kpelj\OneDrive\Desktop\Uni\Year 4\Minor\WebCamAi\yolov3.pt")
#obj_detect.loadModel()
#------------------------------------------------

	#Set webcam parametres
	cam_feed = cv2.VideoCapture(0) 
	cam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, 650)
	cam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 750)
    #Run Camera in the loop

	while True:
		#ret, img = cam_feed.read() # data from camera feed
		#Object detection parametres
		#annotated_image, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",display_percentage_probability=False,display_object_name=True)
		#cv2.imshow("", annotated_image)  #Showing the camera
		ret, frame = cam_feed.read()   
		cv2.imshow('frame', frame)
		 #if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

cam_feed.release()
cv2.destroyAllWindows()

