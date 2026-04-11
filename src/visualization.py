import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

def plot_spectrogram_comparison(original_path, compressed_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.basename(compressed_path).replace(".mp3", "_spec.png")
    output_path = os.path.join(output_dir, filename)

    y_orig, sr = librosa.load(original_path, sr=None)
    y_comp, _ = librosa.load(compressed_path, sr=sr)

    D_orig = librosa.amplitude_to_db(np.abs(librosa.stft(y_orig)), ref=np.max)
    D_comp = librosa.amplitude_to_db(np.abs(librosa.stft(y_comp)), ref=np.max)

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8), layout='constrained')

    img1 = librosa.display.specshow(D_orig, y_axis='hz', x_axis='time', sr=sr, ax=ax[0])
    ax[0].set_title('Original Audio Spectrogram')
    
    img2 = librosa.display.specshow(D_comp, y_axis='hz', x_axis='time', sr=sr, ax=ax[1])
    ax[1].set_title('Compressed Audio Spectrogram')

    fig.colorbar(img1, ax=ax, format='%+2.0f dB', pad=0.02)
    
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def plot_waveform_comparison(original_path, compressed_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.basename(compressed_path).replace(".mp3", "_wave.png")
    output_path = os.path.join(output_dir, filename)

    y_orig, sr = librosa.load(original_path, sr=None)
    y_comp, _ = librosa.load(compressed_path, sr=sr)

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 6), layout='constrained')

    librosa.display.waveshow(y_orig, sr=sr, ax=ax[0], color='blue', alpha=0.7)
    ax[0].set_title('Original Audio Waveform')
    ax[0].set_ylabel('Amplitude')
    
    librosa.display.waveshow(y_comp, sr=sr, ax=ax[1], color='red', alpha=0.7)
    ax[1].set_title('Compressed Audio Waveform')
    ax[1].set_ylabel('Amplitude')

    plt.savefig(output_path)
    plt.close()
    
    return output_path

if __name__ == "__main__":
    orig_file = "data/raw/music/music_orchestra.wav"
    comp_file = "data/encode/music_orchestra_128k.mp3"
    
    spec_dir = "results/spectrogram"
    wave_dir = "results/waveform"
    
    print(f"Extracting features from: {comp_file}")
    
    spec_path = plot_spectrogram_comparison(orig_file, comp_file, spec_dir)
    print(f"Spectrogram saved to: {spec_path}")
    
    wave_path = plot_waveform_comparison(orig_file, comp_file, wave_dir)
    print(f"Waveform saved to: {wave_path}")
