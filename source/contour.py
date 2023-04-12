from imageai.Detection import ObjectDetection # For AI object detection AI
import cv2 # library for the webcam ( this one probably can also find color)
import numpy as np 
cap = cv2.VideoCapture(0)

def getContours(img, imgContour):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  
    for cnt in contours:
        area = cv2.contourArea(cnt) 
        # print(area)#oppervlakte van de figuren
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area>areaMin:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.5, (0,255,0),2)



if __name__ == "__main__":
    
    obj_detect = ObjectDetection()

    while True:
        
        ret, img = cap.read()
        imgcamm, preds = obj_detect.detectObjectsFromImage(input_image=img, output_type="array",
                                                                   display_percentage_probability=False,
                                                                   display_object_name=True)
        

        
        # contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        


        # for obj in preds:
        #     x, y, w, h = obj["box_points"]
        #     cy = int(y+h/2)
        #     cx = int(x+w/2)
        #     pos_label = ("Position: ({}, {})".format(cx, cy))
        #     _, frame = cam_feed.read()
        #     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #     if cy > 479 :
        #         cy = 479

        #     if cx > 639:
        #         cx = 639

        #     pixel_center = hsv_frame[cy, cx]
        #     hue_value = pixel_center[0]

        #     color = "Undefined"
        #     if hue_value < 5:
        #         color = "RED"
        #     elif hue_value < 22:
        #         color = "ORANGE"
        #     elif hue_value < 33:
        #         color = "YELLOW"
        #     elif hue_value < 78:
        #         color = "GREEN"
        #     elif hue_value < 131:
        #         color = "BLUE"
        #     elif hue_value < 170:
        #         color = "VIOLET"
        #     else:
        #         color = "RED"

        #     cv2.putText(annotated_image, color, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 0, 255), 2)
        #     cv2.putText(annotated_image, pos_label, (x , y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



        _, imageFrame = cap.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        success, img = cap.read()

        threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")

        imgContour = img.copy()
        imgBlur = cv2.GaussianBlur(img,(7,7),0)
        imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
        imgCanny = cv2.Canny(imgGray,threshold1,threshold2)

        kernel = np.ones((5,5))
        imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
        
        getContours(imgDil,imgcamm)

        
        # imgStack = stackImages(0.8,([imgContour]))
        # cv2.imshow("Result", imgStack)
        cv2.imshow("ai", imgcamm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   