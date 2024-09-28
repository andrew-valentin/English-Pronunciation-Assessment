import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave

st.title("Voice recording test")

audio_bytes = audio_recorder()
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    wav_file = "audio.wav"

    with open(wav_file, "wb")as f:
        f.write(audio_bytes)

    st.success(f"recording saved")










