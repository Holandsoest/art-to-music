from midiutil.MidiFile import MIDIFile
from midiutil.MidiFile import *
import os

def MakeSong(list):

    def note (pitch, low, high):
        if pitch in forbidden_notes:
            if abs(pitch - low) < abs(pitch - high):
                return pitch + 1 #value closer to low limit so + value
            else:
                return pitch - 1 #value closer to low limit so - value
        else: 
            return pitch #return value as it was

    def addnote(object, channel, pitch, time, duration, volume, instrument, melodie):        
        i = 0
        for i in range(0,4):
            match instrument:
                case "drum":
                    if melodie[i] >= 1:
                        #change pitch for melodie
                        if melodie[i + 4] >= 1:
                            pitch = note(pitch + melodie[i + 4], 69, 86)      
                        midi_drum.addNote(object, channel, pitch, time + melodie[i], duration, volume) # make a note
                case "guitar":
                    if melodie[i] >= 1:
                        #change pitch for melodie
                        if melodie[i + 4] >= 1:
                            pitch = note(pitch + melodie[i + 4], 74, 96)
                        midi_guitar.addNote(object, channel, pitch, time + melodie[i], duration, volume) # make a note
                case "flute":
                    if melodie[i] >= 1:
                        #change pitch for melodie
                        if melodie[i + 4] >= 1:
                            pitch = note(pitch + melodie[i + 4], 72, 108)
                        midi_flute.addNote(object, channel, pitch, time + melodie[i], duration, volume) # make a note
                case "violin":
                    if melodie[i] >= 1:
                        #change pitch for melodie
                        if melodie[i + 4] >= 1:
                            pitch = note(pitch + melodie[i + 4], 76, 103)
                        midi_violin.addNote(object, channel, pitch, time + melodie[i], duration, volume) # make a note
                case "cello":
                    if melodie[i] >= 1:
                        #change pitch for melodie
                        if melodie[i + 4] >= 1:
                            pitch = note(pitch + melodie[i + 4], 48, 77)
                        midi_cello.addNote(object, channel, pitch, time + melodie[i], duration, volume) # make a note
            i += 1        

    #pitch, bpm, duration, volume, instrument, amount
    amount_of_instruments = len(list) # number of object on the screen 
    model_custom_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
    
    # define variables amount
    amount_of_drum = 0
    amount_of_guitar = 0
    amount_of_flute = 0
    amount_of_violin = 0
    amount_of_cello = 0

    object_drum = 0
    object_guitar = 0
    object_flute = 0
    object_violin = 0
    object_cello = 0

    iteration = 0

    #make list for forbidden notes
    forbidden_notes = [22,25,27,30,32,34,42,44,46,49,51,54,56,58,61,63,66,68,70,73,75,78,80,82,85,87,90,92,94,97,99,102,104,106]

    #make melodies
    #first 4 index are for the notes 
    melodie1 = [1,0,0,0, 0,0,0,0] #1000 
    melodie2 = [0,2,0,0, 0,0,0,0] #0100
    melodie3 = [1,2,0,0, 0,-2,0,0] #1100 
    melodie4 = [0,0,3,0, 0,0,0,0] #0010
    melodie5 = [1,0,3,0, 0,0,2,0] #1010
    melodie6 = [0,2,3,0, 0,0,-4,0] #0110
    melodie7 = [1,2,3,0, 0,-2,0,0] #1110
    melodie8 = [0,0,0,4, 0,0,0,0] #0001
    melodie9 = [1,0,0,4, -2,0,0,0] #1001
    melodie10 = [0,2,0,4, 0,0,0,5] #0101
    melodie11 = [1,2,0,4, 0,2,0,4] #1101
    melodie12 = [0,0,3,4, 0,0,0,6] #0011
    melodie13 = [1,0,3,4, 0,0,2,6] #1011
    melodie14 = [0,2,3,4, 0,0,-2,6] #0111
    melodie15 = [1,2,3,4, 0,2,4,6] #1111

    ''' determen melodies        
    (triangle) guitar
    Q1 = melodie 1      Q2 = melodie 2      Q3 = melodie 3       Q4 = melodie 4

    (square / rectangle) drum
    Q1 = melodie 5      Q2 = melodie 6      Q3 = melodie 7       Q4 = melodie 8
    
    (star) cello
    Q1 = melodie 9      Q2 = melodie 10      Q3 = melodie 11       Q4 = melodie 12
    
    (half circle) flute
    Q1 = melodie 13     Q2 = melodie 14      Q3 = melodie 15       Q4 = melodie 1
    
    (heart) piano
    Q1 = melodie 7      Q2 = melodie 8      Q3 = melodie 12       Q4 = melodie 3
    
    (circle) violin
    Q1 = melodie 6      Q2 = melodie 9       Q3 = melodie 8       Q4 = melodie 2   
    '''
    
    # determine the amount of shapes with the same instrument in the list
    for shape in list:
        match shape.instrument:
            case 'drum':    amount_of_drum += 1
            case 'guitar':  amount_of_guitar += 1
            case 'flute':   amount_of_flute += 1
            case 'violin':  amount_of_violin += 1
            case 'cello':   amount_of_cello += 1
            case _: pass
            
    # make midi file for every instrument
    midi_drum = MIDIFile(amount_of_drum, removeDuplicates=False)    
    midi_guitar = MIDIFile(amount_of_guitar, removeDuplicates=False)
    midi_flute = MIDIFile(amount_of_flute, removeDuplicates=False)
    midi_violin = MIDIFile(amount_of_violin, removeDuplicates=False)
    midi_cello = MIDIFile(amount_of_cello, removeDuplicates=False)

    #fill midi files with notes and melodies
    for shape in list:
        
        #add drum notes
        if amount_of_drum > 0 and shape.instrument == "drum":
            
            #check for forbidden notes between 69 and 86
            drum_pitch = note(shape.pitch, 69, 86)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie5
            elif shape.duration == 2: #Q2
                melodie = melodie6
            elif shape.duration == 3: #Q3
                melodie = melodie7
            elif shape.duration == 4: #Q4
                melodie = melodie8

            # add tracks
            time_drum = 0 # time to zero
            channel_drum = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_drum.addTrackName(object_drum, time_drum, f"Track{object_drum}") # give track a name
            midi_drum.addTempo(object_drum, time_drum, shape.bpm) # set bpm
            midi_drum.addProgramChange(object_drum, 0, time_drum, 1) # add instrument = shape.instrument = 1

            addnote(object_drum, channel_drum, drum_pitch, time_drum, shape.duration, shape.volume, "drum", melodie) #add melodie nodes to track#add melodie nodes to track
            object_drum +=1

        #add guitar notes
        if amount_of_guitar > 0 and shape.instrument == "guitar":
            
            #check for forbidden notes between 74 and 96
            guitar_pitch = note(shape.pitch, 74, 96)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie1
            elif shape.duration == 2: #Q2
                melodie = melodie2
            elif shape.duration == 3: #Q3
                melodie = melodie3
            elif shape.duration == 4: #Q4
                melodie = melodie4
            
            # add tracks
            time_guitar = 0 # time to zero
            channel_guitar = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_guitar.addTrackName(object_guitar, time_guitar, f"Track{object_guitar}") # give track a name
            midi_guitar.addTempo(object_guitar, time_guitar, shape.bpm) # set bpm
            midi_guitar.addProgramChange(object_guitar, 0, time_guitar, 1) # add instrument = shape.instrument = 1
         
            addnote(object_guitar, channel_guitar, guitar_pitch, time_guitar, shape.duration, shape.volume, "guitar", melodie) #add melodie nodes to track
            object_guitar +=1

        #add flute notes
        if amount_of_flute > 0 and shape.instrument == "flute":
            
            #check for forbidden notes between 72 and 108
            flute_pitch = note(shape.pitch, 72, 108)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie13
            elif shape.duration == 2: #Q2
                melodie = melodie14
            elif shape.duration == 3: #Q3
                melodie = melodie15
            elif shape.duration == 4: #Q4
                melodie = melodie1
            
            # add tracks
            time_flute = 0 # time to zero
            channel_flute = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_flute.addTrackName(object_flute, time_flute, f"Track{object_flute}") # give track a name
            midi_flute.addTempo(object_flute, time_flute, shape.bpm) # set bpm
            midi_flute.addProgramChange(object_flute, 0, time_flute, 1) # add instrument = shape.instrument = 1

            addnote(object_flute, channel_flute, flute_pitch, time_flute, shape.duration, shape.volume, "flute", melodie) #add melodie nodes to track
            object_flute +=1

        #add violin notes
        if amount_of_violin > 0 and shape.instrument == "violin":
            
            #check for forbidden notes between 76 and 103
            violin_pitch = note(shape.pitch, 76, 103)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie6
            elif shape.duration == 2: #Q2
                melodie = melodie9
            elif shape.duration == 3: #Q3
                melodie = melodie8
            elif shape.duration == 4: #Q4
                melodie = melodie2
                        
            # add tracks
            time_violin = 0 # time to zero
            channel_violin = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_violin.addTrackName(object_violin, time_violin, f"Track{object_violin}") # give track a name
            midi_violin.addTempo(object_violin, time_violin, shape.bpm) # set bpm
            midi_violin.addProgramChange(object_violin, 0, time_violin, 1) # add instrument = shape.instrument = 1

            addnote(object_violin, channel_violin, violin_pitch, time_violin, shape.duration, shape.volume, "violin", melodie) #add melodie nodes to track
            object_violin +=1
        
        #add cello notes
        if amount_of_cello > 0 and shape.instrument == "cello":
            
            #check for forbidden notes between 48 and 77
            cello_pitch = note(shape.pitch, 48, 77)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie5
            elif shape.duration == 2: #Q2
                melodie = melodie10
            elif shape.duration == 3: #Q3
                melodie = melodie11
            elif shape.duration == 4: #Q4
                melodie = melodie12
                        
            # add tracks
            time_cello = 0 # time to zero
            channel_cello = 0 #channel to zero

            # create ass many tracks as objects on the board    
            midi_cello.addTrackName(object_cello, time_cello, f"Track{object_cello}") # give track a name
            midi_cello.addTempo(object_cello, time_cello, shape.bpm) # set bpm
            midi_cello.addProgramChange(object_cello, 0, time_cello, 1) # add instrument = shape.instrument = 1
            
            addnote(object_cello, channel_cello, cello_pitch, time_cello, shape.duration, shape.volume, "cello", melodie)#add melodie nodes to track
            object_cello +=1
        
        #Mmake wav files of all the midi's when al nodes are added
        if amount_of_instruments -1 == iteration:
            #write all the midi files
            with open(model_custom_path + "\\drum_output.mid", "wb") as output_file1: 
                midi_drum.writeFile(output_file1)
            with open(model_custom_path + "\\guitar_output.mid", "wb") as output_file2:
                midi_guitar.writeFile(output_file2)
            with open(model_custom_path + "\\flute_output.mid", "wb") as output_file3:
                midi_flute.writeFile(output_file3)
            with open(model_custom_path + "\\violin_output.mid", "wb") as output_file4:
                midi_violin.writeFile(output_file4)
            with open(model_custom_path + "\\cello_output.mid", "wb") as output_file5:
                midi_cello.writeFile(output_file5)
            
        iteration += 1

    

