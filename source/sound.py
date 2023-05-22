import dawdreamer as daw
from scipy.io import wavfile
from pydub import AudioSegment

import psutil

def AudiRenderPlugin(list):
    sample_rate = 44100
    buffer_size = 128

    
    if psutil.WINDOWS:  absolute_path_plugin = 'C:\\Program Files\\Common Files\\VST3\\BBC Symphony Orchestra (64 Bit).vst3'
    elif psutil.LINUX:  absolute_path_plugin = '' # BUG TODO: 19-invalid-path
    else: raise RuntimeError('That operating system has not been accounted for. Sound.py')

    for instrument in list:
        engine = daw.RenderEngine(sample_rate, buffer_size)
        synth = engine.make_plugin_processor("my_synth", absolute_path_plugin)
        assert synth.get_name() == "my_synth"
        synth.load_state(instrument + "_preset")
        synth.load_midi(instrument +".mid", clear_previous=False, beats=False, all_events=False)

        engine.load_graph([
                        (synth,[])
        ])

        engine.set_bpm(120)
        engine.render(16)  
        audio = engine.get_audio()  
        wavfile.write(instrument + '.wav', sample_rate, audio.transpose()) # Don't forget to transpose!

def AudioWriting():
    # Load the first MP3 file
    sound1 = AudioSegment.from_file("flute.wav", format="wav")
    sound2 = AudioSegment.from_file("drum.wav", format="wav")
    sound3 = AudioSegment.from_file("violin.wav", format="wav")
    sound4 = AudioSegment.from_file("cello.wav", format="wav")
    sound5 = AudioSegment.from_file("guitar.wav", format="wav")

    # Set the desired overlap time in milliseconds
    overlap_time = 16000

    # Extract the overlapping part from the end of the first MP3 file
    overlap_part = sound1[-overlap_time:]
    overlap_part1 = sound2[-overlap_time:]
    overlap_part2 = sound3[-overlap_time:]
    overlap_part3 = sound4[-overlap_time:]

    # Combine the overlapping part of the first MP3 file with the second MP3 file
    combined_sound = overlap_part.overlay(sound5)
    combined_sound2 = overlap_part1.overlay(combined_sound)
    combined_sound3 = overlap_part2.overlay(combined_sound2)
    combined_sound4 = overlap_part3.overlay(combined_sound3)

    # Export the combined audio to an MP3 file
    combined_sound4.export("combined.mp3", format="mp3")

    AudiRenderPlugin()
    AudioWriting()