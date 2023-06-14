import dawdreamer as daw
from scipy.io import wavfile
from pydub import AudioSegment
from pygame import mixer
import typing
import cv2
import time
import os

sample_rate = 44100
buffer_size = 128
model_midi_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
model_preset_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'preset_files')
model_wav_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'wav_files')
model_plugin_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'StupidSimpleSampler')      

def instrument (bpm, instrument):
    engine = daw.RenderEngine(sample_rate, buffer_size)
    synth = engine.make_plugin_processor("my_synth", os.path.join(model_plugin_path, "StupidSimpleSampler.dll"))
    assert synth.get_name() == "my_synth"
    synth.load_state(os.path.join(model_preset_path, f"{instrument}.fxb"))
    synth.load_midi(os.path.join(model_midi_path, f"{instrument}_output.mid"), clear_previous=False, beats=False, all_events=False) 
    #synth.open_editor() #undo # to check if path from plugin is working
    engine.load_graph([
                    (synth,[])
    ])
    engine.set_bpm(bpm)
    engine.render(4/(bpm/60))  
    audio = engine.get_audio()  
    wavfile.write(os.path.join(model_wav_path, f"{instrument}.wav"),  sample_rate, audio.transpose())
       

def audio_rendering(bpm):
    AudioSegment.silent()
    # Load the MP3 files
    sound1 = AudioSegment.from_file(os.path.join(model_wav_path, "drum.wav"), format="wav")
    sound2 = AudioSegment.from_file(os.path.join(model_wav_path, "flute.wav"), format="wav")
    sound3 = AudioSegment.from_file(os.path.join(model_wav_path, "violin.wav"), format="wav")
    sound4 = AudioSegment.from_file(os.path.join(model_wav_path, "clap.wav"), format="wav")
    sound5 = AudioSegment.from_file(os.path.join(model_wav_path, "saxophone.wav"), format="wav")
    sound6 = AudioSegment.from_file(os.path.join(model_wav_path, "guitar.wav"), format="wav")
    sound7 = AudioSegment.from_file(os.path.join(model_wav_path, "piano.wav"), format="wav")

    # Combine the overlapping part of the first MP3 file with the second MP3 file
    combined_sound = sound1.overlay(sound7)
    combined_sound1 = sound2.overlay(combined_sound)
    combined_sound2 = sound3.overlay(combined_sound1)
    combined_sound3 = sound4.overlay(combined_sound2)
    combined_sound4 = sound5.overlay(combined_sound3)
    combined_sound5 = sound6.overlay(combined_sound4)

    combined_sound6 = (combined_sound5 + combined_sound5)*2
    # Export the combined audio to an MP3 file
    with open(os.path.join('files','audio_generator','created_song.mp3'), "wb") as output_file1:
                combined_sound6.export(output_file1, format = "mp3")

def play_loop(song_absolute_path, decay=0.75, cutoff=0.1) -> typing.Any:
    """Uses pygame to play the given music in a blocking manner.  

    Every time it plays the volume decays with the `decay`until it reaches a certain `cutoff` value.
    
    If duding playing you interrupted it with a keystroke it returns the `cv2.type`"""
    mixer.init()
    mixer.music.load(song_absolute_path)
    volume = 1.0
    
    while volume > cutoff:
        mixer.music.set_volume(volume)
        mixer.music.play()
        print(f'Playing music at {volume*100}% volume')
        while mixer.music.get_busy():
            key = cv2.waitKey(1) # time in ms before polling again
            if key != -1:
                mixer.stop()
                mixer.quit()
                return key # `-1` is time expired
        volume = volume * decay
    mixer.quit()
    print('Volume cutoff')
    return -1

if __name__ == "__main__":
    audio_rendering()