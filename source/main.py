# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt

################## Template Matching Example #############
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
import pandas as pd
import argparse

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

#Reading the image with opencv
img = cv2.imread('res.png')
imgColor = cv2.imread('res.png')
imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv(r"C:\Users\mauri\Documents\colors.csv", names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def setNameShape(nameShape, x, y, img):
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        text = nameShape + "\n" + getColorName(r,g,b)
        y0, dy = y, 15
        for i, line in enumerate(text.split('\n')):
            y = y0 + i*dy
            cv2.putText( img, line, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )

ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    x = approx.ravel()[0]
    y = approx.ravel()[1]

    if len(approx) == 3:
        setNameShape("Triangle", x, y, img)
    elif len(approx) == 4 :
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            setNameShape("Square",x,y,img)
        else:
            setNameShape("Rectangle",x,y,img)

    elif len(approx) == 5 :
        setNameShape("Pentagon",x,y,img)
    elif len(approx) == 10 :
        setNameShape("Star",x,y,img)
    else:
        setNameShape("Circle",x,y,img)

while(1):
    cv2.imshow("image",img)

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()