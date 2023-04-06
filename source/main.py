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
        shape.instrument = name  #instrument
        shape.volume = size  #volume
        shape.bpm = color #bpm
        shape.duration = x_axis #duration of note
        shape.pitch = y_axis #pitch

#Create shape listOfShapes
listOfShapes = []

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
    shapeSize = (((width*height)+(imgSize*1))/imgSize)*100

    #Triangle
    if len(approx) == 3:
        colorName = setNameShape("Triangle", int(x), int(y), img)

        #Appending instances to listOfShapes
        #Triangle = Guitar sound = number 30
        #listOfShapes.append(Image("Triangle", int(shapeSize), colorName, int(width), int(height)))
        listOfShapes.append(Image("Guitar", int(shapeSize), 120, 1, 50))

    #Square or rectangle
    elif len(approx) == 4 : 
        x2, y2 , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            colorName = setNameShape("Square",int(x), int(y), img)
            #Square = Drum = number 119
            listOfShapes.append(Image("Drum", int(shapeSize), 60, 2, 200))
        else:
            colorName = setNameShape("Rectangle",int(x), int(y), img)
            #Rectangle = half circle = flute = number 74
            listOfShapes.append(Image("Flute", int(shapeSize), 30, 1, 240))

    #Pentgaon
    elif len(approx) == 5 :
        colorName = setNameShape("Pentagon",int(x), int(y), img)
        #Pentagon = Heartshape = piano = 2
        listOfShapes.append(Image("Piano", int(shapeSize), 240, 2, 100))

    #Star
    elif len(approx) == 10 :
        colorName = setNameShape("Star",int(x), int(y), img)
        #Star = Cello = 43
        listOfShapes.append(Image("Cello", int(shapeSize), 90, 1, 150))

    #Circle
    else:
        colorName = setNameShape("Circle",int(x), int(y),img)
        #Circle = lead 1 = 81
        listOfShapes.append(Image("Violin", int(shapeSize), 120, 1, 200))

# Accessing object value using a for loop
for shape in listOfShapes:
    print("instrument:", shape.instrument, "volume:", shape.volume, "bpm:", shape.bpm, "pitch:", shape.pitch, "duration:", shape.duration, sep='\t')

while(1):
    cv2.imshow("image",img)

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amountOfInstruments = len(list) # number of different insturments
    
    # define variables amount
    amountOfPiano = 0
    amountOfDrum = 0
    amountOfGuitar = 0
    amountOfFlute = 0
    amountOfViolin = 0
    amountOfCello = 0

    objectPiano = 0
    objectDrum = 0
    objectGuitar = 0
    objectFlute = 0
    objectViolin = 0
    objectCello = 0

    iteration = 0

    #determen the amound of shapes woth the same instrument
    for shape in listOfShapes:
        if shape.instrument == "Piano":
            amountOfPiano += 1
        if shape.instrument == "Drum":
            amountOfDrum += 1    
        if shape.instrument == "Guitar":
            amountOfGuitar += 1
        if shape.instrument == "Flute":
            amountOfFlute += 1
        if shape.instrument == "Violin":
            amountOfViolin += 1
        if shape.instrument == "Cello":
            amountOfCello += 1

    # make midi file for every instrument
    midiPiano = MIDIFile(amountOfPiano, removeDuplicates=False)
    midiDrum = MIDIFile(amountOfDrum, removeDuplicates=False)    
    midiGuitar = MIDIFile(amountOfGuitar, removeDuplicates=False)
    midiFlute = MIDIFile(amountOfFlute, removeDuplicates=False)
    midiViolin = MIDIFile(amountOfViolin, removeDuplicates=False)
    midiCello = MIDIFile(amountOfCello, removeDuplicates=False)

    for shape in list:
        
        if amountOfPiano > 0 and shape.instrument == "Piano":
            # add tracks
            timePiano = 0 # time to zero
            channelPiano = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midiPiano.addTrackName(objectPiano, timePiano, f"TrackPiano{objectPiano}") # giva track a name
            midiPiano.addTempo(objectPiano, timePiano, shape.bpm) # set bpm
            midiPiano.addProgramChange(objectPiano, 0, timePiano, shape.instrument) # add insturment
            midiPiano.addNote(objectPiano, channelPiano, shape.pitch, timePiano, shape.duration, shape.volume) # make a note
            
            objectPiano +=1
        
        if amountOfInstruments == iteration:
            #write all the midi files
            with open("PianoOutput.mid", "wb") as output_file:
                midiPiano.writeFile(output_file)
            with open("DrumOutput.mid", "wb") as output_file:
                midiDrum.writeFile(output_file)
            with open("GuitarOutput.mid", "wb") as output_file:
                midiGuitar.writeFile(output_file)
            with open("FluteOutput.mid", "wb") as output_file:
                midiFlute.writeFile(output_file)
            with open("ViolinOutput.mid", "wb") as output_file:
                midiViolin.writeFile(output_file)
            with open("CelloOutput.mid", "wb") as output_file:
                midiCello.writeFile(output_file)
            
        iteration += 1
   
MakeSong(listOfShapes)



