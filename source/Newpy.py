import cv2
import numpy as np

def empty(img):
    pass

video = cv2.VideoCapture(0)
cv2.namedWindow("TrackBar")
cv2.createTrackbar("Area","TrackBar",1000,30000,empty)
cv2.createTrackbar("hue_min","TrackBar",25,179,empty) 
cv2.createTrackbar("hue_max","TrackBar",50,179,empty) 
cv2.createTrackbar("sat_min","TrackBar",105,179,empty) 
cv2.createTrackbar("sat_max","TrackBar",255,255,empty) 
cv2.createTrackbar("val_min","TrackBar",60,255,empty)                
cv2.createTrackbar("val_max","TrackBar",255,255,empty)

def tracking(img):
    height, width, _ = img.shape
    my = int(height/2)
    mx = int(width/2)
    cv2.circle(img, (mx,my),20,(255,0,0),3)

def feedback(img, x,y,w,h):
    cy = int(y+h/2)
    cx = int(x+w/2)
    pos_label = ("Position: ({}, {})".format(cx, cy))
    cv2.putText(img, pos_label, (x , y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)




while True:
    ret,img=video.read()
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    tracking(img)

    hue_min=cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max=cv2.getTrackbarPos ("hue_max", "TrackBar")
    sat_min=cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max=cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min=cv2.getTrackbarPos("val_min", "TrackBar")
    val_max=cv2.getTrackbarPos("val_max", "TrackBar")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    mask=cv2.inRange(hsv, lower, upper)
    cnts,hei=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )
    for c in cnts:
        area = cv2.contourArea(c)
        # str(int(area))
        areaMin = cv2.getTrackbarPos("Area", "TrackBar")        
        if area>areaMin:
            peri = cv2.arcLength(c,True)
            approx=cv2.approxPolyDP(c, 0.02*peri,True)
            x,y,w,h=cv2.boundingRect(c)
            print(str(int(area)))



            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            big_contour = max(contours, key=cv2.contourArea)
            little_contour = min(contours, key=cv2.contourArea)
            area1 = cv2.contourArea(big_contour)
            area1 = cv2.contourArea(big_contour)
            x1,y1,w1,h1 = cv2.boundingRect(big_contour)
            cv2.rectangle(img, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 2)
            # print("red - largest rectangle x,y,w,h,area:",x1,y1,w1,h1,area1)

            area2 = cv2.contourArea(little_contour)
            x2,y2,w2,h2 = cv2.boundingRect(little_contour)
            # cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (0, 255, 0), 2)
            # print("green - smallest rectangle x,y,w,h,area:",x2,y2,w2,h2,area2)

            # save resulting image
            print('2rectangles_result.jpg',img)


            # contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            # print("coins in the image : ", int(len(area)))
            
            # maxi = area
            # big = max(area)
            # print(big)
            # for b in big:
            #     if b > maxi:
            #         maxi = b
                    
            # print("Greatest number: ", maxi)
            # cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
            feedback(img, x,y,w,h)
            print(area)

    cv2.imshow("Frame",img)
    # cv2.imshow("hsv",hsv)
    cv2.imshow("Mask",mask)
    k=cv2.waitKey(1)
    if k==ord('q'):

        break
video. release()
cv2. destroyAllWindows()
