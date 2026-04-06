import os
import librosa
import soundfile as sf

def download_and_prepare_dataset():
    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)  
    print(f"Folder: {output_dir}")
    print("-" * 40)
    audio_samples = {
        'speech_male.wav': 'choice',      
        'speech_female.wav': 'libri1',   
        'music_trumpet.wav': 'trumpet',  
        'music_orchestra.wav': 'brahms'   
    }
    target_sr = 44100  
    for filename, librosa_key in audio_samples.items():
        print(f"Processing file: {filename} (from '{librosa_key}') ...")
        
        try:
            file_path = librosa.ex(librosa_key)
            y, sr = librosa.load(file_path, sr=target_sr)
            save_path = os.path.join(output_dir, filename)
            sf.write(save_path, y, sr)
            
            print(f"The file saved at: {save_path}\n")
        except Exception as e:
            print(f"Error {filename}: {e}\n")

    print("-" * 40)
    print("FINISH!")

if __name__ == "_main_":
    download_and_prepare_dataset()