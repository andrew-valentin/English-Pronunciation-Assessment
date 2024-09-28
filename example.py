import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave
import os

st.title("Voice recording test")

audio_bytes = audio_recorder()

def change_English():
    st.session_state.language = "en-US"
    st.session_state.phrase = "We are transitioning"
    if os.path.exists("audio.wav"):
        os.remove("audio.wav")

    st.write(st.session_state.language)

def change_Spanish():
    st.session_state.language = "es-ES"
    st.session_state.phrase = "Donde esta la biblioteca"
    if os.path.exists("audio.wav"):
        os.remove("audio.wav")
    
    st.write(st.session_state.language)

st.button("EN", on_click=change_English())
st.button("SP", on_click=change_Spanish())

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    wav_file = "audio.wav"

    with open(wav_file, "wb") as f:
        f.write(audio_bytes)

    st.success(f"recording saved")
    from assessment import getAssessment
    result = getAssessment(st.session_state.phrase, st.session_state.language)
    st.write(result)
