import cv2
import pandas as pd
import os
from midiutil.MidiFile import MIDIFile
import pygame
import common.imageProperties as ip

#Declaring global variables
r = g = b = 0

#Create shape listOfShapes
listOfShapes = []

#Reading the image with opencv
img = cv2.imread('imageExample\ExampleShapes6.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Get the height, width and channel of the image
img_height, img_width, channel = img.shape
imgSize = img_height*img_width

#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
absolute_path = os.path.join(os.getcwd(), 'datasets', 'colors.csv')
csv = pd.read_csv(absolute_path, names=index, header=None)

def getBpmFromColor(x_axis, y_axis, image):
    """
    This function gets the RGB values of a pixel on the (x,y)-coordinates of an image and scales this to a number of the table of 30.
    It takes three arguments:
    - x_axis: the x axis coordinate of the pixel
    - y_axis: the y axis coordinate of the pixel
    - image:  the image that will be scanned for the pixel
    
    It returns a scaled value of the table of 30. This number will represent the beats per minute(BPM) of the instrument.
    """
    b, g, r = image[y_axis, x_axis]
    b = int(b)
    g = int(g)
    r = int(r)

    # For now the rgb colorcode will represent a bpm match, but later on we will probably work with colorname to bpm
    # def getShapeColor(R,G,B):
    #     minimum = 10000
    #     for i in range(len(csv)):
    #         d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
    #         if(d<=minimum):
    #             minimum = d
    #             cname = csv.loc[i,"color_name"]
    #     return cname
    
    # colorName = getShapeColor(r,g,b)

    def round_up_to_30(number):
        return min(((number + 29) // 30) * 30, 240)
    
    bpm = round_up_to_30((b + g + r) / 3)
    if bpm < 30:
        return 30
    else:
        return bpm

def getDurationFromWidth(obj_width, img_width):
    """
    This function scales the width of an object in an image relative to the width of the entire image.
    It takes two arguments:
    - obj_width: the width of the object in pixels
    - img_width: the width of the entire image in pixels
    
    It returns a scaled value between 1 and 4 based on the ratio of obj_width to img_width.
    """
    ratio = obj_width / img_width
    if ratio < 0.25:
        return 1
    elif ratio < 0.5:
        return 2
    elif ratio < 0.75:
        return 3
    else:
        return 4

def getVolumeFromSize(obj_size, img_size):
    """
    This function scales the size of an object in an image relative to the size of the entire image.
    It takes two arguments:
    - obj_size: the size of the object in pixels
    - img_size: the size of the entire image in pixels
    
    It returns a scaled value between 20 - 255 based on the ratio of obj_size to img_size.
    It starts at 20 because otherwise the smaller objects wouldnt even make a sound.
    """
    return min((((obj_size)+(img_size*0.2))/img_size)*255, 255)

ret , thrash = cv2.threshold(imgGray, 240 , 255, cv2.CHAIN_APPROX_NONE)
contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#Go through all the contours/shapes that are detected
for contour in contours:
    #get approx contour of shape
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

    #minAreaRect calculates and returns the minimum-area bounding rectangle for a specified point set
    #It will create a rectangle around the shapes
    box = cv2.minAreaRect(contour)
    (x, y), (width, height), angle = box
    #shapeSizeToVolume = (((width*height)+(imgSize*0.2))/imgSize)*255
    shapeSizeToVolume = getVolumeFromSize(width*height, imgSize)
    shapeColorCodeToBpm = getBpmFromColor(int(x),int(y),img)
    shapeWidthToDuration = getDurationFromWidth(width, img_width)
    shapeHeightToPitch = getVolumeFromSize(height, img_height)
    shape = ip.Image(0, int(shapeSizeToVolume), int(shapeColorCodeToBpm), int(shapeWidthToDuration), int(shapeHeightToPitch))

    if len(approx) == 3:
        #Triangle = Guitar sound = number 30
        shape.instrument = 30

    elif len(approx) == 4 : 
        x2, y2 , w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            #Square = Drum = number 119
            shape.instrument = 119
        else:
            # #Rectangle (representing a half circle) = flute = number 74
            shape.instrument = 74

    elif len(approx) == 5 :
        #Pentagon (representing a heartshape) = piano = 2
        shape.instrument = 2

    elif len(approx) == 10 :
        #Star = Cello = 43
        shape.instrument = 43

    else:
        #Circle = lead 1 = 81
        shape.instrument = 81
    
    listOfShapes.append(shape)

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
    amount_of_instruments = len(list)
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
            midi.addTempo(instruments, time, shape.bpm)
            midi.addProgramChange(instruments, 0, time, shape.instrument)
            midi.addNote(track1, channel, shape.pitch, time, shape.duration, shape.volume)
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

MakeSong(listOfShapes)



