from pydub import AudioSegment
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




