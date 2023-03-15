############################### Shape, color and size detection #####################################
import cv2
import pandas as pd
import os

#Declaring global variables
r = g = b = 0

#Declaring class
class Image:
    def __init__(shape, name, size, color, x_axis, y_axis):
        shape.name = name
        shape.size = size
        shape.color = color
        shape.width = x_axis
        shape.height = y_axis

#Create shape list
list = []

#Reading the image with opencv
img = cv2.imread('imageExample\ExampleShapes6.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Get the height(h), width(w) and channel of the image
h, w, c = img.shape
imgSize = h*w

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
absolute_path = os.path.join(os.getcwd(), 'datasets', 'colors.csv')
csv = pd.read_csv(absolute_path, names=index, header=None)

#Function to set the name and color to the shape
def setNameShape(nameShape, x, y, img):
    #Function to calculate minimum distance from all colors and get the most matching color
    def getColorName(R,G,B):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                cname = csv.loc[i,"color_name"]
        return cname
    #Get the RGB color of the pixel in the image at (x,y)
    b,g,r = img[y,x]
    b = int(b)
    g = int(g)
    r = int(r)
    colorName = getColorName(r,g,b)
    text = nameShape + "\n" + colorName
    y0, dy = y, 15
    for i, line in enumerate(text.split('\n')):
        y = y0 + i*dy
        if colorName == "Black":
            cv2.putText( img, line, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255) )
        else:
            cv2.putText( img, line, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
    return colorName

ret , thrash = cv2.threshold(imgGray, 240 , 255, cv2.CHAIN_APPROX_NONE)
contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#Go through all the contours/shapes that are detected
for contour in contours:
    #
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

    #minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
    #It will create a rectangle around the shapes
    box = cv2.minAreaRect(contour)
    (x, y), (width, height), angle = box
    shapeSize = (((width*height)+(imgSize*0.2))/imgSize)*100

    #Triangle
    if len(approx) == 3:
        colorName = setNameShape("Triangle", int(x), int(y), img)

        #Appending instances to list
        list.append(Image("Triangle", int(shapeSize), colorName, int(width), int(height)))

    #Square or rectangle
    elif len(approx) == 4 : 
        x2, y2 , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            colorName = setNameShape("Square",int(x), int(y), img)
            list.append(Image("Square", int(shapeSize), colorName, int(width), int(height)))
        else:
            colorName = setNameShape("Rectangle",int(x), int(y), img)
            list.append(Image("Rectangle", int(shapeSize), colorName, int(width), int(height)))

    #Pentgaon
    elif len(approx) == 5 :
        colorName = setNameShape("Pentagon",int(x), int(y), img)
        list.append(Image("Pentagon", int(shapeSize), colorName, int(width), int(height)))

    #Star
    elif len(approx) == 10 :
        colorName = setNameShape("Star",int(x), int(y), img)
        list.append(Image("Star", int(shapeSize), colorName, int(width), int(height)))

    #Circle
    else:
        colorName = setNameShape("Circle",int(x), int(y),img)
        list.append(Image("Circle", int(shapeSize), colorName, int(width), int(height)))

# Accessing object value using a for loop
for obj in list:
    print(obj.name, obj.size, obj.color, obj.height, obj.width, sep=' ')

while(1):
    cv2.imshow("image",img)

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()