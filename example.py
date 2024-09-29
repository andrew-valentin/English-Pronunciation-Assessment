import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave
import os
from assessment import getAssessment
import pandas as pd
import random

# Read the CSV files
df1 = pd.read_csv('English_phrases_and_sayings.csv', on_bad_lines='skip')
df2 = pd.read_csv('spanishPhrases.csv', on_bad_lines='skip')

# Select a random element
senLength = ""

while (len(senLength) < 10):
    englishPhrase = random.randint(0, len(df1) - 1)
    englishElement = df1.at[englishPhrase, 'text']
    senLength = englishElement.split()

spanishPhrase = random.randint(0, len(df2) - 1)
spanishElement = df2.at[spanishPhrase, 'text']

# Create a button
if st.button('English'):
    st.write(englishElement + '.')

if st.button('Spanish'):
    st.write(spanishElement + '.')

def practiceSwitchCase(language):
    if language == 'English':
        st.session_state.practice_language = "en-US"
        st.session_state.phrase = englishElement + '.'
    if language == 'Spanish':
        st.session_state.practice_language = "es-ES"
        st.session_state.phrase = spanishElement
    if language == 'Chinese (Mandarin, Simplified)':
        st.session_state.practice_language = "zh-CN"
        st.session_state.phrase = "很高兴认识你"
    if language == 'French':
        st.session_state.practice_language = "fr-FR"
        st.session_state.phrase = "Enchanté mon ami. Parlez-vous anglais?"
    if language == 'Italian':
        st.session_state.practice_language = "it-IT"
        st.session_state.phrase = "Mi aiuti, per favore?"
    if language == 'German':
        st.session_state.practice_language = "de-DE"
        st.session_state.phrase = "Ich spreche ein wenig Deutsch."
    if language == 'Japanese':
        st.session_state.practice_language = "ja-JP"
        st.session_state.phrase = "おはようございます"
    if language == 'Russian':
        st.session_state.practice_language = "ru-RU"
        st.session_state.phrase = "Как доехать до вокзала?"

st.title("Language Pronunciation Assessment")

audio_bytes = audio_recorder()

if 'user_language' not in st.session_state:
    st.session_state.user_language = "English"  # Default language

if 'practice_language' not in st.session_state:
    st.session_state.practice_language = "en-US"  # Default language
    st.session_state.phrase = englishElement + '.'

st.session_state.user_language = st.selectbox(
"Select your language: ",
("English", 
 "Spanish",
 "Chinese (Mandarin, Simplified)",
 "French",
 "Italian",
 "German",
 "Japanese",
 "Russian"),
)

st.session_state.practice_language = st.selectbox(
"Select a language to practice: ",
("English", 
 "Spanish",
 "Chinese (Mandarin, Simplified)",
 "French",
 "Italian",
 "German",
 "Japanese",
 "Russian"),
)

st.session_state.user_language = st.session_state.user_language
practiceSwitchCase(st.session_state.practice_language)

st.write(f"Selected Language: {st.session_state.practice_language}")
st.write(f"Now say: {st.session_state.phrase}")

# Create a slider
slider_value = st.slider(
    "How many phrases would you like to practice?",  # Label for the slider
    min_value=0,        # Minimum value
    max_value=15,      # Maximum value
    value=5,           # Default value
    step=1              # Step size
)

# Display the selected value
st.write(f"You selected: {slider_value}")

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    wav_file = "audio.wav"

    with open(wav_file, "wb") as f:
        f.write(audio_bytes)

    st.success(f"recording saved")

    if st.session_state.phrase and st.session_state.user_language and st.session_state.practice_language:
        result = getAssessment(st.session_state.phrase, st.session_state.user_language, st.session_state.practice_language)
        st.markdown(
            f"""
            <div style="background-color: rgb(61 114 213 / 20%); padding: 10px; border-radius: 5px; opacity: 1;">
                {result}
            </div>
            """,
            unsafe_allow_html=True
        )
