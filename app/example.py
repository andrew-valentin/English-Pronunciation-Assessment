import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave
import os
from assessment import getAssessment
import pandas as pd
import random

filename = 'prevPhrase.txt'
content = ''
# Open the file in read mode
def read_file(filename):
    with open(filename, 'r',encoding="utf-8") as file:
        # Read the content of the file
        content = file.read()

read_file(filename)

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

# Example usage
file_path = 'prevPhrase.txt'
if is_file_empty(file_path):
    print("The file is empty.")
else:
    print("The file is not empty.")

# Read the CSV files
df = pd.read_csv('languagePhrases.csv', on_bad_lines='skip')

phraseText = ""

def selectLang(start, end):
    phraseIndex = random.randint(start+1, end-1)
    phraseText = df.at[phraseIndex, 'text']
    if (len(content) == 0):
        with open(filename, 'w',encoding="utf-8") as file:
            file.write(phraseText)
    return phraseText

def practiceSwitchCase(language):
    if language == 'English' or language == "en-US":
        st.session_state.practice_language = "en-US"
        st.session_state.phrase = selectLang(32, 46)
    if language == 'Spanish'or language == "es-ES":
        st.session_state.practice_language = "es-ES"
        st.session_state.phrase = selectLang(0, 15)
    if language == 'Chinese (Mandarin, Simplified)'or language == "zh-CN":
        st.session_state.practice_language = "zh-CN"
        st.session_state.phrase = selectLang(117, 131)
    if language == 'French' or language == "fr-FR":
        st.session_state.practice_language = "fr-FR"
        st.session_state.phrase = selectLang(16, 31)
    if language == 'Italian' or language == "it-IT":
        st.session_state.practice_language = "it-IT"
        st.session_state.phrase = selectLang(47, 61)
    if language == 'German' or language == "de-DE":
        st.session_state.practice_language = "de-DE"
        st.session_state.phrase = selectLang(62,76)
    if language == 'Japanese' or language == "ja-JP":
        st.session_state.practice_language = "ja-JP"
        st.session_state.phrase = selectLang(97,116)
    if language == 'Russian' or language == "ru-RU":
        st.session_state.practice_language = "ru-RU"
        st.session_state.phrase = selectLang(77,96)

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(st.session_state.phrase)

st.title("Language Pronunciation Assessment")

audio_bytes = audio_recorder()


if 'user_language' not in st.session_state:
        st.session_state.user_language = "English"  # Default language

if 'practice_language' not in st.session_state:
    st.session_state.practice_language = "en-US"  # Default language
    st.session_state.phrase = "We are transitioning to the next state."

if 'user_language' not in st.session_state:
    st.session_state.user_language = "English"  # Default language

if 'practice_language' not in st.session_state:
    st.session_state.practice_language = "en-US"  # Default language
    st.session_state.phrase = selectLang(32, 46)

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

# if next was pressed, make sure to use prev lang phrases
if (is_file_empty(file_path)):
    st.write(f"Please say: {st.session_state.phrase}")
else:
    with open('prevLang.txt', 'r',encoding="utf-8") as file:
        prevLang = file.read()
    practiceSwitchCase(prevLang)
    st.write(f"Please say: {st.session_state.phrase}")

# save current language 
if st.button("Another Phrase"):
    with open('prevLang.txt', 'w',encoding="utf-8") as file:
        file.write(st.session_state.practice_language)
else:
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        wav_file = "audio.wav"

        with open(wav_file, "wb") as f:
            f.write(audio_bytes)

        st.success(f"recording saved")

        if st.session_state.phrase and st.session_state.user_language and st.session_state.practice_language:
            result = getAssessment(content, st.session_state.user_language, st.session_state.practice_language)
            st.markdown(
                
                f"""
                <div style="background-color: rgb(61 114 213 / 20%); padding: 10px; border-radius: 5px; opacity: 1;">
                    {result}
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with open(filename, 'w',encoding="utf-8") as file:
            pass  # Doing nothing here effectively clears the file



with open('prevLang.txt', 'w',encoding="utf-8") as file:
    pass