import streamlit as st
import os
import sys
import time # Imported to measure processing latency

# Add the root directory to the system path to allow local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.encoder import encode_audio
from src.metrics import calculate_metrics
from src.visualization import plot_spectrogram_comparison, plot_waveform_comparison

# Set up the main Streamlit page configuration
st.set_page_config(page_title="Audio Codec Analyzer", layout="wide")

st.title("🎵 Project [25201] Evaluating Perceptual Audio Encoding Performance")
# 1. GLOBAL SETTINGS: Users manually choose the mode here
st.sidebar.header("1. Settings")
audio_mode = st.sidebar.selectbox(
    "Select Evaluation Mode:", 
    ["Speech", "Music"], 
    help="Speech mode uses STOI (Intelligibility). Music mode uses Spectral Cosine Similarity."
).lower()

# 2. INPUT DATA: Select source
st.sidebar.header("2. Input Audio")
input_option = st.sidebar.radio("Data Source:", ["Use Sample File", "Upload Custom File (.wav)"])

# Define paths for storage
output_dir = "data/encode"
img_dir = "results"
raw_dir = "data/raw/uploads"

# Ensure directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)
os.makedirs(raw_dir, exist_ok=True)

original_file = None

if input_option == "Use Sample File":
    # Directory path depends on the manually selected global mode
    folder_path = f"data/raw/{audio_mode}"
    
    if os.path.exists(folder_path):
        available_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
        if available_files:
            selected_filename = st.sidebar.selectbox(f"Select {audio_mode.capitalize()} sample:", available_files)
            original_file = os.path.join(folder_path, selected_filename)
        else:
            st.sidebar.error(f"No .wav files found in '{folder_path}'.")
            st.stop()
    else:
        st.sidebar.error(f"Directory not found: {folder_path}")
        st.stop()
else:
    # Logic for custom user uploads
    uploaded_file = st.sidebar.file_uploader("Upload WAV file", type=["wav"])
    if uploaded_file is not None:
        original_file = os.path.join(raw_dir, uploaded_file.name)
        with open(original_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        st.info("Please upload a .wav file from the sidebar to start.")
        st.stop()

# 3. ENCODING CONFIGURATION
st.sidebar.header("3. Encoding Settings")
target_bitrate = st.sidebar.select_slider(
    "Select Target Bitrate (kbps):",
    options=["32k", "64k", "128k", "320k"],
    value="128k"
)

# EXECUTION BLOCK
if st.sidebar.button("Run Analysis"):
    if original_file:
        with st.spinner(f"Processing {audio_mode} audio..."):
            
            # Start timer to calculate latency
            start_time = time.time()
            
            # Execute audio compression via FFmpeg
            results_dict = encode_audio(
                input_filepath=original_file,
                output_dir=output_dir,
                bitrates=[target_bitrate],   
                fmt="mp3"
            )
            
            # End timer and calculate total processing latency
            processing_latency = time.time() - start_time
            
            comp_file = results_dict[target_bitrate]
            
            # Calculate quality metrics using the user-selected mode
            metrics = calculate_metrics(original_file, comp_file, mode=audio_mode)
            
            # Layout for numerical results and players
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Evaluation Metrics")
                st.info(f"Active analysis mode: **{audio_mode.upper()}**")
                
                # Display 5 metrics including the new Latency
                m1, m2, m3 = st.columns(3)
                m1.metric("SNR (dB)", f"{metrics['snr']:.3f}")
                
                # Dynamic labeling based on selected mode
                score_label = "STOI Score" if audio_mode == "speech" else "Cosine Sim."
                m2.metric(score_label, f"{metrics['perceptual_score']:.3f}")
                
                m3.metric("Bitrate (kbps)", f"{metrics['bitrate']/1000:.1f}")

                m4, m5, _ = st.columns(3)
                m4.metric("Compression Ratio", f"{metrics['compression_ratio']:.3f}")
                
                # Added Latency metric
                m5.metric("Latency (s)", f"{processing_latency:.3f}")
                
            with col2:
                st.subheader("🎧 Audio Comparison")
                st.write("Original Source:")
                st.audio(original_file)
                st.write(f"Encoded Output ({target_bitrate}):")
                st.audio(comp_file)

        # Visualizations
        st.subheader("Visual Analysis")
        tab1, tab2 = st.tabs(["Spectrogram Comparison", "Waveform Comparison"])
        
        with tab1:
            spec_path = plot_spectrogram_comparison(original_file, comp_file, os.path.join(img_dir, "spectrogram"))
            st.image(spec_path, use_container_width=True)
        with tab2:
            wave_path = plot_waveform_comparison(original_file, comp_file, os.path.join(img_dir, "waveform"))
            st.image(wave_path, use_container_width=True)
    else:
        st.error("No valid audio file selected.")
else:
    st.info("Configure parameters in the sidebar and click 'Run Analysis' to begin.")