# Python code for Multiple Color Detection  
import numpy as np
import cv2
  
# # Capturing video through webcam
# webcam = cv2.VideoCapture(0)
# # Start a while loop


# def kleuren():
#     red_lower = np.array([136, 87, 111], np.uint8)
#     red_upper = np.array([180, 255, 255], np.uint8)
#     red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
  
#     green_lower = np.array([25, 52, 72], np.uint8)
#     green_upper = np.array([102, 255, 255], np.uint8)
#     green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
  
#     blue_lower = np.array([94, 80, 2], np.uint8)
#     blue_upper = np.array([120, 255, 255], np.uint8)
#     blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

#     # lower_orange = np.array([5, 100, 100], np.uint8)
#     # upper_orange = np.array([15, 255, 255], np.uint8)
#     # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

#     # lower_green = np.array([36, 25, 25], np.uint8)
#     # upper_green = np.array([86, 255, 255], np.uint8)
#     # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

#     # lower_blue = np.array([110, 50, 50], np.uint8)
#     # upper_blue = np.array([130, 255, 255], np.uint8)
#     # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

#     # lower_violet = np.array([140, 50, 50], np.uint8)
#     # upper_violet = np.array([160, 255, 255], np.uint8)
#     # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

#     # lower_red1 = np.array([0, 50, 50], np.uint8)
#     # upper_red1 = np.array([10, 255, 255], np.uint8)
#     # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

#     # lower_red2 = np.array([170, 50, 50], np.uint8)
#     # upper_red2 = np.array([180, 255, 255], np.uint8)
#     # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

#     kernel = np.ones((5, 5))
      
#     # For red color
#     red_mask = cv2.dilate(red_mask, kernel)

#     # For green color
#     green_mask = cv2.dilate(green_mask, kernel)

#     # For blue color
#     blue_mask = cv2.dilate(blue_mask, kernel)

#     # Creating contour to track red color
#     contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      
#     for pic, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area > 300):
#             x, y, w, h = cv2.boundingRect(contour)
#             #imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),  (0, 0, 255), 2)
#             cv2.putText(imageFrame, "Red Colour", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))    
  
#     # Creating contour to track green color
#     contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      
#     for pic, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area > 300):
#             x, y, w, h = cv2.boundingRect(contour)
#             cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
  
#     # Creating contour to track blue color
#     contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     for pic, contour in enumerate(contours):
#         area = cv2.contourArea(contour)
#         if(area > 300):
#             x, y, w, h = cv2.boundingRect(contour)
#             #imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h),(255, 0, 0), 2)
#             cv2.putText(imageFrame, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (255, 0, 0))

# while(1):
      
#     _, imageFrame = webcam.read()
#     hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
  
#     kleuren()
#     # Program Termination
#     cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
#     if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
#         break

# cv2.destroyAllWindows()








# img = cv2.imshow("red.jpg")
# print(img)
# cv2.imshow("img", img)
# cv2.waitKey(0)


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def kleur():
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)
    # Pick pixel value

    pixel_center = hsv_frame[cy, cx]

    hue_value = pixel_center[0]
    print(hue_value)

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

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
    cv2.imshow("Frame", frame)

while True:
    kleur()
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()




# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while(1):

#     # Take each frame
#     _, frame = cap.read()

#     # Convert BGR to HSV
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     # define range of blue color in HSV
#     lower_blue = np.array([110,50,50])
#     upper_blue = np.array([130,255,255])

#     # Threshold the HSV image to get only blue colors
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Bitwise-AND mask and original image
#     res = cv2.bitwise_and(frame,frame, mask= mask)

#     cv2.imshow('frame',frame)
#     cv2.imshow('mask',mask)
#     cv2.imshow('res',res)
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break

# cv2.destroyAllWindows()