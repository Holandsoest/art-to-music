from midiutil.MidiFile import MIDIFile

def MakeSong(list):
    #pitch, bpm, duration, volume, instrument, amount
    amount_of_instruments = len(list) # number of object on the screen 
    
    # define variables amount
    amount_of_piano = 0
    amount_of_drum = 0
    amount_of_guitar = 0
    amount_of_flute = 0
    amount_of_violin = 0
    amount_ofcello = 0

    object_piano = 0
    object_drum = 0
    object_guitar = 0
    object_flute = 0
    object_violin = 0
    object_cello = 0

    iteration = 0

    #determen the amound of shapes woth the same instrument
    for shape in listOfShapes:
        if shape.instrument == "Piano":
            amount_of_piano += 1
        if shape.instrument == "Drum":
            amount_of_drum += 1    
        if shape.instrument == "Guitar":
            amount_of_guitar += 1
        if shape.instrument == "Flute":
            amount_of_flute += 1
        if shape.instrument == "Violin":
            amount_of_violin += 1
        if shape.instrument == "Cello":
            amount_ofcello += 1

    # make midi file for every instrument
    midi_piano = MIDIFile(amount_of_piano, removeDuplicates=False)
    midi_drum = MIDIFile(amount_of_drum, removeDuplicates=False)    
    midi_guitar = MIDIFile(amount_of_guitar, removeDuplicates=False)
    midi_flute = MIDIFile(amount_of_flute, removeDuplicates=False)
    midi_violin = MIDIFile(amount_of_violin, removeDuplicates=False)
    midi_cello = MIDIFile(amount_ofcello, removeDuplicates=False)

    for shape in list:
        
        if amount_of_piano > 0 and shape.instrument == "Piano":
            # add tracks
            time_piano = 0 # time to zero
            channel_piano = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_piano.addTrackName(object_piano, time_piano, f"TrackPiano{object_piano}") # giva track a name
            midi_piano.addTempo(object_piano, time_piano, shape.bpm) # set bpm
            midi_piano.addProgramChange(object_piano, 0, time_piano, shape.instrument) # add insturment
            midi_piano.addNote(object_piano, channel_piano, shape.pitch, time_piano, shape.duration, shape.volume) # make a note
            
            object_piano +=1
        
        if amount_of_instruments == iteration:
            #write all the midi files
            with open("PianoOutput.mid", "wb") as output_file:
                midi_piano.writeFile(output_file)
            with open("DrumOutput.mid", "wb") as output_file:
                midi_drum.writeFile(output_file)
            with open("GuitarOutput.mid", "wb") as output_file:
                midi_guitar.writeFile(output_file)
            with open("FluteOutput.mid", "wb") as output_file:
                midi_flute.writeFile(output_file)
            with open("ViolinOutput.mid", "wb") as output_file:
                midi_violin.writeFile(output_file)
            with open("CelloOutput.mid", "wb") as output_file:
                midi_cello.writeFile(output_file)
            
        iteration += 1