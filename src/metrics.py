#nesseccary libraries
import numpy as np
import os
import time
import librosa
from scipy.signal import correlate
from pystoi import stoi

# a constant to prevent division by zero errors
a = 1e-12

# ALIGN SIGNALS 
def align_signals(x, y):
    corr = correlate(y, x, method='fft')  #cross - correlation
    # using "fft" - fast fourier tranform to faster for long audio file with the complexity O(NlogN)
    # calculate the phase shift (lag) between the two signals
    lag = np.argmax(corr) - (len(x) - 1)
    # at the maximum cross-correlation, the two signals are most similar.
    # trim the signals based on the lag to make them overlap
    if lag > 0:
        y = y[lag:]
    elif lag < 0:
        x = x[-lag:]
    # ensure both arrays have the exact same length
    min_len = min(len(x), len(y))
    x, y = x[:min_len], y[:min_len]
    return x, y

# SNR
def calculate_snr(x, y):
    noise = x - y # the difference between the original signal and the reconstructed signal
    signal_power = np.mean(x**2)    
    noise_power = np.mean(noise**2) + a
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# BITRATE 
def calculate_bitrate(file_path, duration):
    file_size_bits = os.path.getsize(file_path) * 8
    return file_size_bits / duration

# PERCEPTUAL QUALITY SCORE
def calculate_perceptual_score(x, y, sr, mode):
    if mode == "speech":
        return stoi(x, y, sr, extended=False)
    else:
        # Convert to frequency domain using STFT
        X = np.abs(librosa.stft(x))
        Y = np.abs(librosa.stft(y))
        num = np.sum(X * Y)
        de = np.sqrt(np.sum(X**2)) * np.sqrt(np.sum(Y**2)) + a
        return num / de # Cosine similarity in STFT
def calculate_metrics(original_path, compressed_path, mode="speech"):
    x, sr = librosa.load(original_path, sr=16000)
    y, _ = librosa.load(compressed_path, sr=16000)
    x_aligned, y_aligned = align_signals(x, y)
    duration = len(y_aligned) / sr
    snr_val = calculate_snr(x_aligned, y_aligned)
    br_val = calculate_bitrate(compressed_path, duration)
    score_val = calculate_perceptual_score(x_aligned, y_aligned, sr, mode)
    cr_val = os.path.getsize(original_path) / (os.path.getsize(compressed_path) + 1e-12)
    
    return {
        "snr": snr_val,
        "bitrate": br_val,
        "perceptual_score": score_val,
        "compression_ratio": cr_val
    }
if __name__ == "__main__":
    original_path = "data/raw/music/music_orchestra.wav"
    encoded_path  = "data/encode/music_orchestra_64k.mp3"
    # Mode selection
    mode = "music" 
    print("Processing audio... please wait.")

    #Load the original file
    x, sr = librosa.load(original_path, sr=16000)
    y, _ = librosa.load(encoded_path, sr=16000)

    # Align signals once 
    x_aligned, y_aligned = align_signals(x, y)

    # Run the metrics
    duration = len(y_aligned) / sr
    snr_value = calculate_snr(x_aligned, y_aligned)
    br_value = calculate_bitrate(encoded_path, duration)
    score = calculate_perceptual_score(x_aligned, y_aligned, sr, mode)
    
    # Compression Ratio
    compression_ratio = os.path.getsize(original_path) / os.path.getsize(encoded_path)

    # Display Results
    print(f"EVALUATION RESULTS ({mode.upper()})")
    print(f"SNR:               {snr_value:.2f} dB")
    print(f"Bitrate:           {br_value/1000:.2f} kbps")
    print(f"Perceptual Score:  {score:.4f}")
    print(f"Compression Ratio: {compression_ratio:.2f}")
