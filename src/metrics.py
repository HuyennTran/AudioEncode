import numpy as np
import os
from scipy.signal import correlate
from pystoi import stoi   
import librosa

# align
def align_signals(x, y):
    corr = correlate(y, x)
    lag = np.argmax(corr) - len(x) + 1
    if lag > 0:
        y = y[lag:]
    else:
        x = x[-lag:]
    min_len = min(len(x), len(y))
    return x[:min_len], y[:min_len]
# SNR
def snr_db(x, y):
    x, y = align_signals(x, y)
    noise = x - y
    return 10 * np.log10(np.sum(x**2) / (np.sum(noise**2) + 1e-12))
# bittrate
def bitrate(file_path, signal, sr):
    size_bits = os.path.getsize(file_path) * 8
    duration = len(signal) / sr
    return size_bits / duration
# perceptual
def perceptual_score(x, y, sr):
    x, y = align_signals(x, y)
    return stoi(x, y, sr)

if __name__ == "__main__":
    original_path = "../data/raw/speech/speech_male.wav"
    encoded_path  = "../data/encode/speech_male_64k.mp3"

    x, sr = librosa.load(original_path, sr=16000)
    y, _ = librosa.load(encoded_path, sr=16000)

    snr = snr_db(x, y)
    br = bitrate(encoded_path, y, sr)
    stoi_score = perceptual_score(x, y, sr)

    print("RESULT")
    print(f"SNR (dB): {snr:.2f}")
    print(f"Bitrate (bps): {br:.2f}")
    print(f"STOI: {stoi_score:.4f}")