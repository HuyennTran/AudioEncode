import os
import numpy as np
import librosa

def calculate_compression_ratio(original_path, compressed_path):
    try:
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)
        return original_size / compressed_size
    except FileNotFoundError as e:
        print(f"File error: {e}")
        return 0

def calculate_snr(original_path, compressed_path):
    try:
        y_orig, sr = librosa.load(original_path, sr=None)
        y_comp, _ = librosa.load(compressed_path, sr=sr)

        min_len = min(len(y_orig), len(y_comp))
        y_orig = y_orig[:min_len]
        y_comp = y_comp[:min_len]

        noise = y_orig - y_comp
        signal_power = np.sum(y_orig ** 2)
        noise_power = np.sum(noise ** 2)

        if noise_power == 0:
            return float('inf')

        snr = 10 * np.log10(signal_power / noise_power)
        return snr
    except Exception as e:
        print(f"Calculation error: {e}")
        return 0

if __name__ == "__main__":
    orig_file = "data/raw/music/music_orchestra.wav"
    comp_file = "data/encode/music_orchestra_128k.mp3"
    
    print(f"Analyzing: {comp_file} vs {orig_file}")
    
    cr = calculate_compression_ratio(orig_file, comp_file)
    snr = calculate_snr(orig_file, comp_file)
    
    print(f"Compression Ratio: {cr:.2f}")
    print(f"SNR: {snr:.2f} dB")