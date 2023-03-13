############################### Shape and color detection #####################################
import cv2
import pandas as pd
import os

#declaring global variables
r = g = b = 0

#Reading the image with opencv
img = cv2.imread('imageExample\ExampleShapes.png')
imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
absolute_path = os.path.join(os.getcwd(), 'datasets', 'colors.csv')
csv = pd.read_csv(absolute_path, names=index, header=None)

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#function to set the name and color to the shape
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

    #Triangle
    if len(approx) == 3: 
        setNameShape("Triangle", x, y, img)
    #Square or rectangle
    elif len(approx) == 4 : 
        x, y , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            setNameShape("Square",x,y,img)
        else:
            setNameShape("Rectangle",x,y,img)
    #Pentgaon
    elif len(approx) == 5 :
        setNameShape("Pentagon",x,y,img)
    #Star
    elif len(approx) == 10 :
        setNameShape("Star",x,y,img)
    #Circle
    else:
        setNameShape("Circle",x,y,img)

while(1):
    cv2.imshow("image",img)

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()