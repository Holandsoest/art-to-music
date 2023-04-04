import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)




def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",159,255,empty)
cv2.createTrackbar("Threshold2","Parameters",53,255,empty)
cv2.createTrackbar("Area","Parameters",180,30000,empty)






def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt) 
        # print(area)#oppervlakte van de figuren
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area>areaMin:

            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri) 
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(len(approx)) #total points of ervery figure
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(cnt)
            # cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

            _, area= cap.read()
            hsvFrame = cv2.cvtColor(area, cv2.COLOR_BGR2HSV)

            # Pick pixel value
            pixel_center = hsvFrame[x, y]
            hue_value = pixel_center[0]
            color = "Undefined"
            if hue_value < 5:
                color = "RED"
            elif hue_value < 22:
                color = "ORANGE"
            elif hue_value < 33:
                color = "YELLOW"
            elif hue_value < 78:
                color = "GREEN"
            elif hue_value < 131:
                color = "BLUE"
            elif hue_value < 170:
                color = "VIOLET"
            else:
                color = "RED"
            # print(color)


            #pixel_center_bgr = frame[cy, cx]
            #b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
            

            #cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
            #cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
            cv2.putText(imgContour, "Color: " + str(len("color")), (x + w +20, y + 50), cv2.FONT_HERSHEY_COMPLEX,0.7, (0,255,0),2)
            cv2.circle(imgContour, (x, y), 5, (25, 25, 25), 3)
            #cv2.imshow("Frame", frame)
            # cv2.circle(imgContour, (x, y),5, (x+w,y+h), (25, 25, 25), 2)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w +20, y + 20), cv2.FONT_HERSHEY_COMPLEX,0.7, (0,255,0),2)


           





            
            #cv2.putText(imgContour, "color: " + str(color) ,(x + w +20, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)  
    
            # if objCor ==3: objectType ="Tri"
            # elif objCor == 4:
            #     aspRatio = w/float(h)
            #     if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
            #     else:objectType="Rectangle"
            # elif objCor>4: objectType= "Circles"
            # else:objectType="None"
 
            # cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            # cv2.putText(imgContour,objectType,
            #             (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
            #             (0,0,0),2)


while True:
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
    
    getContours(imgDil,imgContour)

    # imgStack = stackImages(0.8,([img,imgCanny,imgCanny],[imgContour,imgContour,imgContour]))
    imgStack = stackImages(0.8,([imgContour]))
    cv2.imshow("Result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


     # cx = int(x / 2)
            # cy = int(y / 2)
            # # Pick pixel value
            # pixel_center = hsvFrame[cy, cx]
            # # print(pixel_center)
            # print(hsvFrame)
            # hue_value = pixel_center[0]
            # color = "Undefined"
            # print(pixel_center[0])
            # red_lower = np.array([136, 87, 111], np.uint8)
            # red_upper = np.array([180, 255, 255], np.uint8)
            # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
            # green_lower = np.array([25, 52, 72], np.uint8)
            # green_upper = np.array([102, 255, 255], np.uint8)
            # green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
         
            # blue_lower = np.array([94, 80, 2], np.uint8)
            # blue_upper = np.array([120, 255, 255], np.uint8)
            # blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
            # # For red color

            # kernel = np.ones((5, 5))
            # red_mask = cv2.dilate(red_mask, kernel)
            # green_mask = cv2.dilate(green_mask, kernel)
            # blue_mask = cv2.dilate(blue_mask, kernel)

            # contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # for pic, contour in enumerate(contours):
            #     x, y, w, h = cv2.boundingRect(contour)
            #     area = cv2.contourArea(contour)
            #     color = "RED"
            # contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
            # for pic, contour in enumerate(contours):
            #     x, y, w, h = cv2.boundingRect(contour)
            #     area = cv2.contourArea(contour)
            #     color = "green"
            
            # contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # for pic, contour in enumerate(contours):
            #     x, y, w, h = cv2.boundingRect(contour)
            #     area = cv2.contourArea(contour)
            #     color = "blue"
            # if 136 < pixel_center[0] < 180 & 87 < pixel_center[1] < 255 & 111 < pixel_center[2] < 255:
            #     color = "RED"
            # elif 25 < pixel_center[0] < 102 & 52 < pixel_center[1] < 255 & 72 < pixel_center[2] < 255:
            #     color = "ORANGE"
            # elif 94 < pixel_center[0] < 120 & 80 < pixel_center[1] < 255 & 2 < pixel_center[2] < 255:
            #     color = "YELLOW"
            # elif hue_value < 78:
            #     color = "GREEN"
            # elif hue_value < 131:
            #     color = "BLUE"
            # elif hue_value < 170:
            #     color = "VIOLET"
            # else:
            #     color = "RED"
            # print(hue_value)
            #print(color)
            