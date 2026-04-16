import os
import yaml
import argparse
from pydub import AudioSegment

def encode_audio(input_filepath, output_dir, bitrates=["32k", "64k", "128k", "320k"], fmt="mp3"):
    # Ensure the target directory exists before saving files
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract the original filename without the extension for output naming
    base_name = os.path.basename(input_filepath).replace(".wav", "")
    
    try:
        # Load the raw audio data into memory for processing
        audio = AudioSegment.from_wav(input_filepath)
    except Exception as e:
        print(f"Error loading {input_filepath}: {e}")
        return {}

    encoded_paths = {}
    
    # Process and export the audio for each requested bitrate
    for bitrate in bitrates:
        output_filename = f"{base_name}_{bitrate}.{fmt}"
        output_filepath = os.path.join(output_dir, output_filename)
        
        # Perform the actual compression and save the output file
        audio.export(output_filepath, format=fmt, bitrate=bitrate)
        
        # Store the resulting file path in the dictionary for reference
        encoded_paths[bitrate] = output_filepath
        
    return encoded_paths

if __name__ == "__main__":
    # Configure command-line argument parsing for batch processing
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=str, required=True)
    args = parser.parse_args()
    
    config_path = args.config
    
    try:
        # Load encoding parameters from the specified YAML configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"File not found: {config_path}")
        exit()

    # Extract specific configuration values from the parsed YAML data
    settings = config["encode_settings"]
    input_file = settings["input_filepath"]
    output_folder = settings["output_dir"]
    bitrates_list = settings["bitrates"]
    audio_format = settings["format"]
    
    print(f"Processing file: {input_file}...")
    
    # Execute the encoding pipeline using the parsed settings
    results = encode_audio(
        input_filepath=input_file, 
        output_dir=output_folder, 
        bitrates=bitrates_list, 
        fmt=audio_format
    )
    
    # Display the final output paths to the console
    print("\nResults:")
    for br, path in results.items():
        print(f"Bitrate {br} -> {path}")