import os
import librosa
import soundfile as sf

def download_and_prepare_dataset():
    # Define the base directory for storing raw audio data
    base_dir = os.path.join("data", "raw")
    print(f"Base Folder: {base_dir}")
    
    # Mapping of target filenames to Librosa sample dataset keys
    # Key 'libri1' provides a speech sample, 'brahms' provides an orchestral music sample
    audio_samples = {
        'speech_male.wav': 'libri1',       
        'music_orchestra.wav': 'brahms'   
    }
    
    # Set a standard high-fidelity sampling rate for evaluation
    target_sr = 44100  
    
    for filename, librosa_key in audio_samples.items():
        print(f"Processing file: {filename} (from '{librosa_key}') ...")
        
        # Categorize files into 'speech' or 'music' subfolders based on filename prefix
        if filename.startswith('speech'):
            output_dir = os.path.join(base_dir, 'speech')
        else:
            output_dir = os.path.join(base_dir, 'music')
            
        # Create the subdirectories if they do not already exist
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Retrieve the local path of the Librosa example file
            file_path = librosa.ex(librosa_key)
            
            # Load the audio data and resample it to the target sampling rate
            y, sr = librosa.load(file_path, sr=target_sr)
            
            # Construct the final destination path and write the file as a WAV
            save_path = os.path.join(output_dir, filename)
            sf.write(save_path, y, sr)
            
            print(f"The file saved at: {save_path}\n")
        except Exception as e:
            # Catch and display any errors during download or processing
            print(f"Error processing {filename}: {e}\n")

    print("DATASET PREPARATION FINISHED!")

if __name__ == "__main__":
    # Execute the preparation script
    download_and_prepare_dataset()