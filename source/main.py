# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt

################## Template Matching #############
# img_rgb = cv.imread("res.png")
# img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
# template = cv.imread(r"C:\Users\mauri\Documents\BlueTriangle.png",0)
# w, h = template.shape[::-1]
# res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
# threshold = 0.8
# loc = np.where( res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)

# cv.imwrite('res.png',img_rgb)
# cv.imshow('image', img_rgb)
# cv.waitKey(0)

############################### Shape detection #####################################
import numpy as np
import cv2

img = cv2.imread('res.png')
imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 3:
        print("Triangle x,y", x, y)
        cv2.putText( img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
    elif len(approx) == 4 :
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        #print(aspectRatio)
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            print("Square x,y", x, y)
        else:
            cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            print("Rectangle x,y", x, y)

    elif len(approx) == 5 :
        cv2.putText(img, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 10 :
        cv2.putText(img, "star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    else:
        cv2.putText(img, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

cv2.imshow('shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import cv2
# import numpy as np
# import pandas as pd
# import argparse

# #Creating argument parser to take image path from command line
# # ap = argparse.ArgumentParser()
# # ap.add_argument('-i', '--image', required=True, help="Image Path")
# # args = vars(ap.parse_args())
# # img_path = args['image']

# #Reading the image with opencv
# img = cv2.imread(r"C:\Users\mauri\Documents\colorpic.jpg")

# #declaring global variables (are used later on)
# clicked = False
# r = g = b = xpos = ypos = 0

# #Reading csv file with pandas and giving names to each column
# index=["color","color_name","hex","R","G","B"]
# csv = pd.read_csv(r"C:\Users\mauri\Documents\colors.csv", names=index, header=None)

# #function to calculate minimum distance from all colors and get the most matching color
# def getColorName(R,G,B):
#     minimum = 10000
#     for i in range(len(csv)):
#         d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
#         if(d<=minimum):
#             minimum = d
#             cname = csv.loc[i,"color_name"]
#     return cname

# #function to get x,y coordinates of mouse double click
# def draw_function(event, x,y,flags,param):
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         print("buttonClicked")
#         global b,g,r,xpos,ypos, clicked
#         clicked = True
#         xpos = x
#         ypos = y
#         b,g,r = img[y,x]
#         b = int(b)
#         g = int(g)
#         r = int(r)
       
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_function)

# while(1):

#     cv2.imshow("image",img)
#     if (clicked):
   
#         #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
#         cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

#         #Creating text string to display( Color name and RGB values )
#         text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
#         #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
#         cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

#         #For very light colours we will display text in black colour
#         if(r+g+b>=600):
#             cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
#         clicked=False

#     #Break the loop when user hits 'esc' key    
#     if cv2.waitKey(20) & 0xFF ==27:
#         break
    
# cv2.destroyAllWindows()