import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave

st.title("Voice recording test")

audio_bytes = audio_recorder()

st.session_state.clicked = "us-EN"


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Click me', on_click=click_button)

# if st.session_state.clicked:
#     # The message and nested widget will remain on the page
#     st.write('Button clicked!')
#     st.slider('Select a value')

session = False

def change_English():
    st.session_state.clicked = "us-EN"

def change_Spanish():
    st.session_state.clicked = "es-ES"

if st.button("EN", on_click=change_English()):
    language = "en-US"
    phrase = "We are transitioning"
    st.write(language)
    st.write("Now say: " + phrase)
if st.button("SP", on_click=change_Spanish()):
    language = "es-ES"
    phrase = "Donde esta la biblioteca"
    st.write(language)
    st.write("Now say: " + phrase)

# st.write(language)
# st.write("Now say: " + phrase)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    wav_file = "audio.wav"

    with open(wav_file, "wb")as f:
        f.write(audio_bytes)

    st.success(f"recording saved")
    from assessment import getAssessment
    result = getAssessment(phrase, language)
    st.write(result)
