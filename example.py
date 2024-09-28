import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave
import os
from assessment import getAssessment

st.title("Voice recording test")

audio_bytes = audio_recorder()

if 'language' not in st.session_state:
    st.session_state.language = "en-US"  # Default language
    st.session_state.phrase = "We are transitioning to the next state."

if st.button("EN"):
    st.session_state.language = "en-US"
    st.session_state.phrase = "We are transitioning to the next state."
if st.button("SP"):
    st.session_state.language = "es-ES"
    st.session_state.phrase = "Donde esta la biblioteca?"
if st.button("FR"):
    st.session_state.language = "fr-FR"
    st.session_state.phrase = "Enchanté mon ami. Parlez-vous anglais?"
if st.button("IT"):
    st.session_state.language = "it-IT"
    st.session_state.phrase = "Mi aiuti, per favore?"
if st.button("JP"):
    st.session_state.language = "ja-JP"
    st.session_state.phrase = "おはようございます"

st.write(f"Selected Language: {st.session_state.language}")
st.write(f"Now say: {st.session_state.phrase}")

# audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    wav_file = "audio.wav"

    with open(wav_file, "wb") as f:
        f.write(audio_bytes)

    st.success(f"recording saved")

    if st.session_state.phrase and st.session_state.language:
        result = getAssessment(st.session_state.phrase, st.session_state.language)
        st.write(result)
