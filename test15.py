from midiutil.MidiFile import MIDIFile
import pygame

def MakeSong(pitch, bpm, duration, volume, instrument, amount_of_instruments):
    # create MIDIFile object
    midi = MIDIFile(amount_of_instruments, removeDuplicates=False)

    time = 0
    channel = 0
    instruments = 0

    while instruments < amount_of_instruments:
        # create ass many tracks as instruments
        midi.addTrackName(instruments, time, f"Track{instruments}")
        midi.addTempo(instruments, time, bpm)
        midi.addProgramChange(instruments, 0, time, instrument)

        midi.addNote(instruments, channel, pitch, time, duration, volume)
        instruments +=1

    with open("output.mid", "wb") as output_file:
        midi.writeFile(output_file)
    pygame.mixer.init()

    # load MIDI file
    pygame.mixer.music.load("output.mid")

    # play MIDI file
    pygame.mixer.music.play()

    # wait for music to finish playing
    while pygame.mixer.music.get_busy():
        continue

class object:
    def __init__(self, pitch, bpm, duration, volume, instrument):
        self.pitch = pitch
        self.bpm = bpm
        self.duration = duration
        self.volume = volume
        self.instrument = instrument

p1 = object(60, 120, 2, 255, 50)
p2 = object(50, 120, 2, 40, 30)
p3 = object(25, 120, 2, 30, 40)
amount_of_instruments = 1

MakeSong()