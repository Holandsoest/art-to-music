############################### Shape, color and size detection #####################################
import cv2
import pandas as pd
import os
from midiutil.MidiFile import MIDIFile
import pygame

#Declaring global variables
r = g = b = 0

#Declaring class
class Image:
    def __init__(shape, name, size, color, x_axis, y_axis):
        shape.name = name  #instrument
        shape.size = size  #volume
        shape.color = color #bpm
        shape.width = x_axis #duration of note
        shape.height = y_axis #pitch

#Create shape listOfShapes
listOfShapes = []

#Reading the image with opencv
img = cv2.imread('imageExamples\ExampleShapes6.png')
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

        #Appending instances to listOfShapes
        listOfShapes.append(Image("Triangle", int(shapeSize), colorName, int(width), int(height)))

    #Square or rectangle
    elif len(approx) == 4 : 
        x2, y2 , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            colorName = setNameShape("Square",int(x), int(y), img)
            listOfShapes.append(Image("Square", int(shapeSize), colorName, int(width), int(height)))
        else:
            colorName = setNameShape("Rectangle",int(x), int(y), img)
            listOfShapes.append(Image("Rectangle", int(shapeSize), colorName, int(width), int(height)))

    #Pentgaon
    elif len(approx) == 5 :
        colorName = setNameShape("Pentagon",int(x), int(y), img)
        listOfShapes.append(Image("Pentagon", int(shapeSize), colorName, int(width), int(height)))

    #Star
    elif len(approx) == 10 :
        colorName = setNameShape("Star",int(x), int(y), img)
        listOfShapes.append(Image("Star", int(shapeSize), colorName, int(width), int(height)))

    #Circle
    else:
        colorName = setNameShape("Circle",int(x), int(y),img)
        listOfShapes.append(Image("Circle", int(shapeSize), colorName, int(width), int(height)))

# Accessing object value using a for loop
for shape in listOfShapes:
    print(shape.name, shape.size, shape.color, shape.height, shape.width, sep=' ')
    
while(1):
    cv2.imshow("image",img)

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amount_of_instruments = list.count()
    for shape in list:

        # create MIDIFile object
        midi = MIDIFile(amount_of_instruments, removeDuplicates=False)

        # add tracks
        track1 = 0
        time = 0
        channel = 0 
        instruments = 0

        while instruments < amount_of_instruments:
        # create ass many tracks as instruments        
            midi.addTrackName(instruments, time, f"Track{instruments}")
            midi.addTempo(instruments, time, list.color)
            midi.addProgramChange(instruments, 0, time, list.name)

            midi.addNote(track1, channel, list.y_axis, time, list.x_axis, list.size)
            time = +2
            instruments +=1

        with open("output.mid", "wb") as output_file:
            midi.writeFile(output_file)
        
        pygame.mixer.init()
        #load MIDI file
        pygame.mixer.music.load("output.mid")
        # play MIDI file
        pygame.mixer.music.play()
        # wait for music to finish playing
        while pygame.mixer.music.get_busy():
            continue

#MakeSong(pitch=60, bpm=120, duration=2, volume=255, instrument=4, amount=1)
#MakeSong(pitch=80, bpm=120, duration=2, volume=200, instrument=100, amount=2)
MakeSong(listOfShapes)



