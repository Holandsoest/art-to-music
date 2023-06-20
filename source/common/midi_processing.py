from pydub import AudioSegment
import typing
import cv2
import time
import os
import sf2_loader as sf

model_midi_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'midi_files')
model_wav_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'wav_files')
model_font_path = os.path.join(os.getcwd(), 'files', 'audio_generator', 'soundfonts')
   
def instrument (bpm, instrument):
    loader = sf.sf2_loader(os.path.join(model_font_path, f"{instrument}.sf2"))
    loader.change(channel=0, bank=0, preset=0) # change current preset number to 0
    loader.export_midi_file(os.path.join(model_midi_path, f"{instrument}_output.mid"), name=os.path.join(model_wav_path, f"{instrument}.wav"), format='wav', show_msg=True)

def audio_rendering(bpm):
    total_time=(4/(bpm/60))*1000
   
    # Load the MP3 files
    sound1 = AudioSegment.from_file(os.path.join(model_wav_path, "drum.wav"), format="wav", duration=total_time)
    sound2 = AudioSegment.from_file(os.path.join(model_wav_path, "flute.wav"), format="wav", duration=total_time)
    sound3 = AudioSegment.from_file(os.path.join(model_wav_path, "violin.wav"), format="wav", duration=total_time)
    sound4 = AudioSegment.from_file(os.path.join(model_wav_path, "clap.wav"), format="wav", duration=total_time)
    sound5 = AudioSegment.from_file(os.path.join(model_wav_path, "saxophone.wav"), format="wav", duration=total_time)
    sound6 = AudioSegment.from_file(os.path.join(model_wav_path, "guitar.wav"), format="wav", duration=total_time)
    sound7 = AudioSegment.from_file(os.path.join(model_wav_path, "piano.wav"), format="wav", duration=total_time)
    sound8 = AudioSegment.silent(duration=total_time)

    # Combine the overlapping part of the first MP3 file with the second MP3 file
    combined_sound = sound8.overlay(sound1)
    combined_sound1 = combined_sound.overlay(sound2)
    combined_sound2 = combined_sound1.overlay(sound3)
    combined_sound3 = combined_sound2.overlay(sound4)
    combined_sound4 = combined_sound3.overlay(sound5)
    combined_sound5 = combined_sound4.overlay(sound6)
    combined_sound6 = combined_sound5.overlay(sound7)

    combined_sound7 = (combined_sound6 + combined_sound6)*2
    # Export the combined audio to an MP3 file
    with open(os.path.join('files','audio_generator','created_song.mp3'), "wb") as output_file1:
                combined_sound7.export(output_file1, format = "mp3")

def play_loop(song_absolute_path, decay=0.75, cutoff=0.1) -> typing.Any:
    """Uses pygame to play the given music in a blocking manner.  

    Every time it plays the volume decays with the `decay`until it reaches a certain `cutoff` value.
    
    If during playing you interrupted it with a keystroke it returns the [`typing.`key](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7) """
    from pygame import mixer

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
