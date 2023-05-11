from midiutil.MidiFile import MIDIFile
from midiutil.MidiFile import *
import os

'''
alle bpm naar geiddelde 60 naar 120 
size is volume
we gaan niet meer naar melodie maar naar losse noot
'''

def MakeSong(list):

    # --- define functions ---
    def forbidden_note (pitch, low, high): # function to check if a note is not forbidden

        if pitch in forbidden_notes:
            if abs(pitch - low) < abs(pitch - high):
                return pitch + 1 #value closer to low limit so + value
            else:
                return pitch - 1 #value closer to low limit so - value
        else: 
            return pitch #return value as it was

    def add_note (object, channel, pitch, time, duration, volume, instrument, melodie): # function for adding one note to midi file       
        
        # function variables
        i = 0

        for i in range(0,4): # go over all melodie moments (every second)
            
            if melodie[i] >= 1:
                match instrument:
                    case "kick":     
                        midi_kick.addNote(object, channel, pitch, time + melodie[i], duration, volume) # add a note
                    case "clap":
                        midi_clap.addNote(object, channel, pitch, time + melodie[i], duration, volume) # add a note 

        i += 1

    def add_accord(object, channel, pitch, volume, instrument, melodie): # function for adding one accord to midi file       
        
        # init varibles
        i = 0
        time = 0
        first_cycle = 1

        for i in range(0,80): # check all the notes with steek of 20
            
            pitch_note_1 = pitch # input pitch level
            pitch_note_2 = 0
            pitch_note_3 = 0
            duration_notes = 0

            #add loop of 4 to check in one mate
            i2 = 0
            for i2 in range(0,4):

                if first_cycle:
                    time = time # don't update time
                else:
                    time = time + 0.25 # update time

                if melodie[i + i2] > 0: # we need to add 3 notes now to make an accord
                    
                    pitch_note_1 = pitch_note_1 + melodie[i+4] #assign pitch value note 1
                    pitch_note_2 = pitch_note_1 + melodie[i+8] #assign pitch value note 2
                    pitch_note_3 = pitch_note_1 + melodie[i+12] #assign pitch value note 3

                    duration_notes = duration_notes + melodie[i+16] #assing duration of notes

                    match instrument:
                        # ----- mid -----    
                        case "piano":
                            midi_piano.addNote(object, channel, pitch_note_1, time, duration_notes, volume) # make a note
                            midi_piano.addNote(object, channel, pitch_note_2, time, duration_notes, volume) # make a note
                            midi_piano.addNote(object, channel, pitch_note_3, time, duration_notes, volume) # make a note

                        case "guitar":
                            midi_guitar.addNote(object, channel, pitch_note_1, time, duration_notes, volume) # make a note
                            midi_guitar.addNote(object, channel, pitch_note_2, time, duration_notes, volume) # make a note
                            midi_guitar.addNote(object, channel, pitch_note_3, time, duration_notes, volume) # make a note
    
                    pitch_note_1 = pitch #input pitch level
                    pitch_note_2 = 0
                    pitch_note_3 = 0
                    
            i += 20       

    # --- melodies ---
    # kick melodies 4 diff
    kick_melodie0 = [0,0,0,0] #empty melodie
    kick_melodie1 = [1,0,3,0] 
    kick_melodie2 = [0,2,0,4] 
    kick_melodie3 = [1,0,0,4] 
    kick_melodie4 = [1,2,3,4] 

    # clap melodies 4 diff
    clap_melodie0 = [0,0,0,0] #empty melodie
    clap_melodie1 = [1,0,3,0] 
    clap_melodie2 = [0,2,0,4] 
    clap_melodie3 = [1,0,0,4] 

    # --- declare variables
    model_custom_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
    amount_of_instruments = len(list) # number of object on the screen  
    iteration = 0 # used to go over all the shapes in the pictures   
    
    # define variables amount and objects
    # --- high --- single
    amount_of_flute = 0 
    object_flute = 0    
    amount_of_violin = 0 # could also be mid
    object_violin = 0 # could also be mid    
    # --- mid --- accord
    amount_of_guitar = 0    
    object_guitar = 0
    amount_of_piano = 0
    object_piano = 0
    # --- low --- single 
    amount_of_drum = 0    
    object_drum = 0
    amount_of_saxophone = 0  
    object_saxophone = 0
    # --- kick --- single
    amount_of_kick = 0
    object_kick = 0
    # --- clap --- single
    amount_of_clap = 0    
    object_clap = 0
    # --- bpm ---
    bpm = 0
    
    # scale notes
    def scale (percentage, instrument):
        flute_low = 50 # C???
        flute_high = 100
        
        match instrument:
            case 'flute':
                return forbidden_note (((percentage/100) * (flute_high - flute_low) + flute_low), flute_low, flute_high) # check if note is forbidden or not




    # make list for forbidden notes
    def guitar_notes (percentage, note_1, note_2, note_3):
        match percentage:
            case range(50,60): # C?
                note_1 = 60
                note_2 = 67
                note_3 = 73

    forbidden_notes = [22,25,27,30,32,34,42,44,46,49,51,54,56,58,61,63,66,68,70,73,75,78,80,82,85,87,90,92,94,97,99,102,104,106]

    '''
        #high melodies. 

        #mid melodies. 

        #low melodies. 
        low_melodie0 = [    0,0,0,0,    0,0,0,0,    0,0,0,0,    0,0,0,0,   0,0,0,0,   #maat 1 
                            0,0,0,0,    0,0,0,0,    0,0,0,0,    0,0,0,0,   0,0,0,0,   #maat 2 
                            0,0,0,0,    0,0,0,0,    0,0,0,0,    0,0,0,0,   0,0,0,0,   #maat 3 
                            0,0,0,0,    0,0,0,0,    0,0,0,0,    0,0,0,0,   0,0,0,0,   #maat 4 
                        ]
        low_melodie1 = [    1,0,0,0,    0,0,0,0,    7,0,0,0,    12,0,0,0,   0.5,0,0,0,      #maat 1  eerste stuk van viva la vida
                            1,0,0,0,    0,0,0,0,    7,0,0,0,    12,0,0,0,   0.25,0,0,0,     #maat 2 
                            1,0,0,0,    0,0,0,0,    7,0,0,0,    12,0,0,0,   0.25,0,0,0,     #maat 3 
                            1,0,0.5,0,  0,0,2,0,    7,0,5,0,    12,0,5,0,   0.25,0,0.5,0,   #maat 4 
                        ]

                      
        melodie division = steek of 20 
        #0 t/m 3    -   20 t/m 23   -   => notes
        #4 t/m 7    -   24 t/m 27   -   => pitch note 1 
        #8 t/m 11   -   28 t/m 31   -   => pitch diffence note 2
        #12 t/m 15  -   32 t/m 35   -   => pitch diffence note 3
        #16 t/m 19  -   36 t/m 39   -   => durations of notes
        
    '''
    
    # determine the amount of shapes with the same instrument in the list
    for shape in list:
        match shape.instrument:
            case 'flute':   
                amount_of_flute += 1
                bpm = bpm + shape.bpm 
            case 'violin':  
                amount_of_violin += 1
                bpm = bpm + shape.bpm 
            case 'guitar':  
                amount_of_guitar += 1
                bpm = bpm + shape.bpm    
            case 'piano':   
                amount_of_piano += 1
                bpm = bpm + shape.bpm 
            case 'drum':  
                amount_of_drum += 1
                bpm = bpm + shape.bpm 
            case 'saxophone':  
                amount_of_saxophone += 1
                bpm = bpm + shape.bpm 
            case 'kick':  
                amount_of_kick += 1
                bpm = bpm + shape.bpm 
            case 'clap':   
                amount_of_clap += 1
                bpm = bpm + shape.bpm 
            
            case _: pass        

    bpm = bpm/amount_of_instruments # determen bpm of composition

    # make midi file for every instrument
    midi_flute          = MIDIFile(amount_of_flute,     removeDuplicates=False) # high
    midi_violin         = MIDIFile(amount_of_violin,    removeDuplicates=False) # high 
    midi_guitar         = MIDIFile(amount_of_guitar,    removeDuplicates=False) # mid
    midi_piano          = MIDIFile(amount_of_piano,     removeDuplicates=False) # mid
    midi_drum           = MIDIFile(amount_of_drum,      removeDuplicates=False) # low     
    midi_saxophone      = MIDIFile(amount_of_saxophone, removeDuplicates=False) # low     
    midi_kick           = MIDIFile(amount_of_kick,      removeDuplicates=False) # kick
    midi_clap           = MIDIFile(amount_of_clap,      removeDuplicates=False) # clap
    
    # -----------flute / high-----------
    # add tracks
    time_flute = 0 # time to zero
    channel_flute = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_flute.addTrackName(object_flute, time_flute, f"Track{object_flute}") # give track a name
    midi_flute.addTempo(object_flute, time_flute, bpm) # set bpm
    midi_flute.addProgramChange(object_flute, 0, time_flute, 1) # add instrument = shape.instrument = 1

    # -----------violin / high-----------
    # add tracks
    time_violin = 0 # time to zero
    channel_violin = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_flute.addTrackName(object_violin, time_violin, f"Track{object_violin}") # give track a name
    midi_flute.addTempo(object_violin, time_violin, bpm) # set bpm
    midi_flute.addProgramChange(object_violin, 0, time_violin, 1) # add instrument = shape.instrument = 1

    # -----------guitar / mid-----------
    # add tracks
    time_guitar = 0 # time to zero
    channel_guitar = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_guitar.addTrackName(object_guitar, time_guitar, f"Track{object_guitar}") # give track a name
    midi_guitar.addTempo(object_guitar, time_guitar, bpm) # set bpm
    midi_guitar.addProgramChange(object_guitar, 0, time_guitar, 1) # add instrument = shape.instrument = 1

    # -----------piano / mid-----------
    # add tracks
    time_piano = 0 # time to zero
    channel_piano = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_piano.addTrackName(object_piano, time_piano, f"Track{object_piano}") # give track a name
    midi_piano.addTempo(object_piano, time_piano, bpm) # set bpm
    midi_piano.addProgramChange(object_piano, 0, time_piano, 1) # add instrument = shape.instrument = 1

    # -----------drum / low-----------
    # add tracks
    time_drum = 0 # time to zero
    channel_drum = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_drum.addTrackName(object_drum, time_drum, f"Track{object_drum}") # give track a name
    midi_drum.addTempo(object_drum, time_drum, bpm) # set bpm
    midi_drum.addProgramChange(object_drum, 0, time_drum, 1) # add instrument = shape.instrument = 1

    # -----------saxophone / low-----------
    # add tracks
    time_saxophone = 0 # time to zero
    channel_saxophone = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_saxophone.addTrackName(object_saxophone, time_saxophone, f"Track{object_saxophone}") # give track a name
    midi_saxophone.addTempo(object_saxophone, time_saxophone, bpm) # set bpm
    midi_saxophone.addProgramChange(object_saxophone, 0, time_saxophone, 1) # add instrument = shape.instrument = 1

    # -----------kick-----------
    # add tracks
    time_kick = 0 # time to zero
    channel_kick = 0 #channel to zero

    # create ass many tracks as objects on the board    
    midi_kick.addTrackName(object_kick, time_kick, f"Track{object_kick}") # give track a name
    midi_kick.addTempo(object_kick, time_kick, bpm) # set bpm
    midi_kick.addProgramChange(object_kick, 0, time_kick, 1) # add instrument = shape.instrument = 1

    # -----------clap-----------
    # add tracks
    time_clap = 0 # time to zero
    channel_clap = 0 #channel to zero
    # create ass many tracks as objects on the board    
    midi_clap.addTrackName(object_clap, time_clap, f"Track{object_clap}") # give track a name
    midi_clap.addTempo(object_clap, time_clap, bpm) # set bpm
    midi_clap.addProgramChange(object_clap, 0, time_clap, 1) # add instrument = shape.instrument = 1
    
    #fill midi files with notes
    for shape in list:
        
        #add flute notes
        if amount_of_flute > 0 and shape.instrument == "flute":
            
            # getal
            flute_pitch = shape.duration

            addnote(object_drum, channel_drum, drum_pitch, time_drum, shape.duration, shape.volume, "drum", melodie) #add melodie nodes to track#add melodie nodes to track
            object_drum +=1


        #add kick notes
        if amount_of_kick > 0 and shape.instrument == "kick":
            
            drum_pitch = 100

            

            addnote(object_drum, channel_drum, drum_pitch, time_drum, shape.duration, shape.volume, "drum", melodie) #add melodie nodes to track#add melodie nodes to track
            object_drum +=1

        #add guitar notes
        if amount_of_guitar > 0 and shape.instrument == "guitar":
            
            #check for forbidden notes between 74 and 96
            guitar_pitch = note(shape.pitch, 74, 96)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie
            elif shape.duration == 2: #Q2
                melodie = melodie
            elif shape.duration == 3: #Q3
                melodie = melodie
            elif shape.duration == 4: #Q4
                melodie = melodie

            addnote(object_guitar, channel_guitar, guitar_pitch, time_guitar, shape.duration, shape.volume, "guitar", melodie) #add melodie nodes to track
            object_guitar +=1

        #add flute notes
        if amount_of_flute > 0 and shape.instrument == "flute":
            
            #check for forbidden notes between 72 and 108
            flute_pitch = note(shape.pitch, 72, 108)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie
            elif shape.duration == 2: #Q2
                melodie = melodie
            elif shape.duration == 3: #Q3
                melodie = melodie
            elif shape.duration == 4: #Q4
                melodie = melodie

            addnote(object_flute, channel_flute, flute_pitch, time_flute, shape.duration, shape.volume, "flute", melodie) #add melodie nodes to track
            object_flute +=1

        #add violin notes
        if amount_of_violin > 0 and shape.instrument == "violin":
            
            #check for forbidden notes between 76 and 103
            violin_pitch = note(shape.pitch, 76, 103)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie
            elif shape.duration == 2: #Q2
                melodie = melodie
            elif shape.duration == 3: #Q3
                melodie = melodie
            elif shape.duration == 4: #Q4
                melodie = melodie

            addnote(object_violin, channel_kick, violin_pitch, time_kick, shape.duration, shape.volume, "violin", melodie) #add melodie nodes to track
            object_violin +=1
        
        #add cello notes
        if amount_of_cello > 0 and shape.instrument == "cello":
            
            #check for forbidden notes between 48 and 77
            cello_pitch = note(shape.pitch, 48, 77)

            #choose melodie
            if shape.duration == 1: #Q1
                melodie = melodie
            elif shape.duration == 2: #Q2
                melodie = melodie
            elif shape.duration == 3: #Q3
                melodie = melodie
            elif shape.duration == 4: #Q4
                melodie = melodie
                        
            addnote(object_cello, channel_clap, cello_pitch, time_clap, shape.duration, shape.volume, "cello", melodie)#add melodie nodes to track
            object_cello +=1    
        
        #Mmake wav files of all the midi's when al nodes are added
        if amount_of_instruments -1 == iteration:
            if amount_of_drum == 0:
                addnote(object_drum, channel_drum, 0, time_drum, 0, 0, "drum", melodie0) #clear track
            if amount_of_guitar == 0:
                addnote(object_guitar, channel_guitar, 0, time_guitar, 0, 0, "guitar", melodie0) #clear track
            if amount_of_flute == 0:
                addnote(object_flute, channel_flute, 0, time_flute, 0, 0, "flute", melodie0) #clear track
            if amount_of_violin == 0:
                addnote(object_violin, channel_kick, 0, time_kick, 0, 0, "violin", melodie0) #clear track
            if amount_of_cello == 0:
                addnote(object_cello, channel_clap, 0, time_clap, 0, 0, "cello", melodie0) #clear track

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

    

