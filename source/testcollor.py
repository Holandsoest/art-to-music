import numpy as np
import cv2
  
while(1):
    _, imageFrame = webcam.read()
    x, y, w, h = cv2.boundingRect(contour)
    webcam = cv2.VideoCapture(0)
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
  
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    kernel = np.ones((5, 5))
    # For red color
    red_mask = cv2.dilate(red_mask, kernel)
 
    # For green color
    green_mask = cv2.dilate(green_mask, kernel)

    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernel)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 300):
            #print(contour)
            collor = "BLUE"

    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate():
        area = cv2.contourArea(contour)
        if(area > 300):
            # Pick pixel value
            collor = "BLUE"

            #imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),  (0, 0, 255), 2)

    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate():
        area = cv2.contourArea(contour)
        if(area > 300):
            collor = "BLUE"
 
    cv2.putText(imageFrame, collor , (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))    
              
    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
        break

cv2.destroyAllWindows()
