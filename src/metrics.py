import os
import numpy as np
from scipy.signal import correlate
from pystoi import stoi
import librosa

def align_signals(x, y):
    corr = correlate(y, x)
    lag = np.argmax(corr) - len(x) + 1
    if lag > 0:
        y = y[lag:]
    else:
        x = x[-lag:]
    min_len = min(len(x), len(y))
    return x[:min_len], y[:min_len]

def snr_db(x, y):
    x, y = align_signals(x, y)
    noise = x - y
    return 10 * np.log10(np.sum(x**2) / (np.sum(noise**2) + 1e-12))

def calculate_bitrate(file_path, signal, sr):
    size_bits = os.path.getsize(file_path) * 8
    duration = len(signal) / sr
    return size_bits / duration

def perceptual_score(x, y, sr):
    x, y = align_signals(x, y)
    return stoi(x, y, sr)

def calculate_metrics(original_path, compressed_path):
    x, sr = librosa.load(original_path, sr=16000)
    y, _ = librosa.load(compressed_path, sr=16000)
    
    snr_val = snr_db(x, y)
    br_val = calculate_bitrate(compressed_path, y, sr)
    stoi_val = perceptual_score(x, y, sr)
    
    return {
        "snr": snr_val,
        "bitrate": br_val,
        "stoi": stoi_val
    }

if __name__ == "__main__":
    test_original = "data/raw/music/music_orchestra.wav"
    test_encoded  = "data/encode/music_orchestra_128k.mp3"
    if os.path.exists(test_original) and os.path.exists(test_encoded):
        print(f"Analyzing:\n- Orig: {test_original}\n- Comp: {test_encoded}\n")
        results = calculate_metrics(test_original, test_encoded)
        print("=== TEST RESULTS ===")
        print(f"SNR (dB): {results['snr']:.2f}")
        print(f"Bitrate (bps): {results['bitrate']:.0f}")
        print(f"STOI: {results['stoi']:.4f}")
    else:
        print("Test files not found. Please ensure the files exist in data/ folders.")