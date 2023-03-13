from midiutil.MidiFile import MIDIFile
import pygame

def MakeSong(pitch, bpm, duration, volume, instrument, amount):
    # create MIDIFile object
    midi = MIDIFile(1, removeDuplicates=False)

    # add tracks
    track1 = 0
    time = 0
    channel = 0 

    # create track 1
    midi.addTrackName(track1, time, "Track 1")
    midi.addTempo(track1, time, bpm)
    midi.addProgramChange(track1, channel, time, instrument)

    # track 1 notes
    for i in range(4):
        time = i * duration
        midi.addNote(track1, channel, pitch, time, duration, volume)
        midi.addNote(track1, channel, pitch+4, time, duration, volume)
        midi.addNote(track1, channel, pitch+7, time, duration, volume)
        time = i * duration
        pitch = pitch + 1

    with open(f"output{amount}.mid", "wb") as output_file:
        midi.writeFile(output_file)

MakeSong(pitch=60, bpm=120, duration=2, volume=255, instrument=4, amount=1)
MakeSong(pitch=80, bpm=120, duration=2, volume=200, instrument=100, amount=2)

mid1 = MIDIFile("output1.mid")
mid2 = MIDIFile("output2.mid")

merged_mid = MIDIFile(2, removeDuplicates=False)
# Copy time resolution. (If mid1 and mid2 have different
# ticks_per_beat you will get timing problems.)
merged_mid.ticks_per_beat = mid1.ticks_per_beat

merged_mid.tracks = mid1.tracks + mid2.tracks
merged_mid.save('merged.mid')