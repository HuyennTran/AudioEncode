import streamlit as st
import os
import sys

# Add the root directory to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.encoder import encode_audio
from src.metrics import calculate_metrics
from src.visualization import plot_spectrogram_comparison, plot_waveform_comparison

# Configure the Streamlit application layout
st.set_page_config(page_title="Audio Codec Analyzer", layout="wide")

st.title("🎵 Audio Encoding & Quality Evaluation Dashboard")
st.markdown("Project: Audio Encoding Performance Evaluation")

# Section 1: Input Data Source
st.sidebar.header("1. Input Audio")
input_option = st.sidebar.radio("Data Source:", ["Use Sample File", "Upload Custom File (.wav)"])

# Define directory paths
output_dir = "data/encode"
img_dir = "results"
raw_dir = "data/raw/uploads"

# Create necessary directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)
os.makedirs(raw_dir, exist_ok=True)

# Initialize audio mode variable for metrics calculation
audio_mode = "speech"

if input_option == "Use Sample File":
    input_type = st.sidebar.selectbox("Select Audio Type:", ["Speech", "Music"])
    audio_mode = input_type.lower()
    folder_path = f"data/raw/{audio_mode}"
    
    # Load sample files dynamically
    if os.path.exists(folder_path):
        available_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
        if available_files:
            selected_filename = st.sidebar.selectbox(f"Select {input_type} file:", available_files)
            original_file = os.path.join(folder_path, selected_filename)
        else:
            st.sidebar.error(f"No .wav files found in '{folder_path}'.")
            st.stop()
    else:
        st.sidebar.error(f"Directory not found: {folder_path}")
        st.stop()
else:
    # Handle custom uploads and determine content type
    uploaded_file = st.sidebar.file_uploader("Upload WAV file", type=["wav"])
    audio_mode = st.sidebar.selectbox("Select Audio Content Type:", ["speech", "music"])
    
    if uploaded_file is not None:
        original_file = os.path.join(raw_dir, uploaded_file.name)
        with open(original_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        st.info("Please upload a .wav file from the sidebar to start.")
        st.stop()

# Section 2: Encoding Configuration
st.sidebar.header("2. Encoding Settings")
target_bitrate = st.sidebar.select_slider(
    "Select Target Bitrate (kbps):",
    options=["32k", "64k", "128k", "320k"],
    value="128k"
)

# Section 3: Execution and Analysis
if st.sidebar.button("Run Analysis"):
    with st.spinner("Processing audio..."):
        
        # Compress the audio file
        results_dict = encode_audio(
            input_filepath=original_file,
            output_dir=output_dir,
            bitrates=[target_bitrate],   
            fmt="mp3"
        )
        
        comp_file = results_dict[target_bitrate]
        
        # Calculate all evaluation metrics using the selected mode
        metrics = calculate_metrics(original_file, comp_file, mode=audio_mode)
        
        # Render the results layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Evaluation Metrics")
            
            # Display first row of metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("SNR (dB)", f"{metrics['snr']:.3f}")
            m2.metric("Perceptual Score", f"{metrics['perceptual_score']:.3f}")
            m3.metric("Bitrate (bps)", f"{metrics['bitrate']:.0f}")
            m4.metric("Compression Ratio", f"{metrics['compression_ratio']:.3f}")
            # Display second row of metrics
        with col2:
            st.subheader("🎧 Audio Comparison")
            st.write("Original (.wav):")
            st.audio(original_file)
            st.write(f"Compressed ({target_bitrate} MP3):")
            st.audio(comp_file)

        st.divider()

        # Generate and render visual comparisons
        st.subheader("📊 Visual Analysis")
        
        tab1, tab2 = st.tabs(["Spectrogram", "Waveform"])
        
        with tab1:
            spec_path = plot_spectrogram_comparison(original_file, comp_file, os.path.join(img_dir, "spectrogram"))
            st.image(spec_path, use_container_width=True)
            
        with tab2:
            wave_path = plot_waveform_comparison(original_file, comp_file, os.path.join(img_dir, "waveform"))
            st.image(wave_path, use_container_width=True)
else:
    st.info("Click 'Run Analysis' to start processing.")