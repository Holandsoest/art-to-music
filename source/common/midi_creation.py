from midiutil.MidiFile import MIDIFile

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amountOfInstruments = len(list) # number of object on the screen 
    
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