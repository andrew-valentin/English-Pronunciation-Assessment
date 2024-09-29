import streamlit as st
from audio_recorder_streamlit import audio_recorder
from assessment import getAssessment
from google.cloud import texttospeech
import google.auth
import google.cloud.secretmanager
import tempfile
import os
import pandas as pd
import random

secrets = google.cloud.secretmanager.SecretManagerServiceClient()
google_name = 'projects/pronunciation-assessment-2024/secrets/google_credentials/versions/latest'
google_secret = secrets.access_secret_version(name=google_name)
google_payload = google_secret.payload.data.decode("UTF-8")

# Save the JSON secret to a temporary file
with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
    temp_file.write(google_payload)
    temp_file_path = temp_file.name

creds, project = google.auth.load_credentials_from_file(temp_file_path)

# Open the file in read mode
def read_file(filename):
    with open(filename, 'r',encoding="utf-8") as file:
        # Read the content of the file
        content = file.read()

def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0

@st.cache_data
def selectLang(df, content, filename, start, end):
    phraseIndex = random.randint(start+1, end-1)
    phraseText = df.at[phraseIndex, 'text']
    if (len(content) == 0):
        with open(filename, 'w',encoding="utf-8") as file:
            file.write(phraseText)
    return phraseText

@st.cache_data
def practiceSwitchCase(df, content, filename, language):
    if language == 'English':
        st.session_state.practice_language = "en-US"
        st.session_state.speaker = "en-US-Standard-A"
        phrase = selectLang(df, content, filename, 32, 46)
    if language == 'Spanish':
        st.session_state.practice_language = "es-ES"
        st.session_state.speaker = "es-ES-Standard-A"
        phrase = selectLang(df, content, filename, 0, 15)
    if language == 'Chinese (Mandarin, Simplified)':
        st.session_state.practice_language = "zh-CN"
        st.session_state.speaker = "cmn-CN-Standard-A"
        phrase = selectLang(df, content, filename, 117, 131)
    if language == 'French':
        st.session_state.practice_language = "fr-FR"
        st.session_state.speaker = "fr-FR-Standard-A"
        phrase = selectLang(df, content, filename, 16, 31)
    if language == 'Italian':
        st.session_state.practice_language = "it-IT"
        st.session_state.speaker = "it-IT-Standard-C"
        phrase = selectLang(df, content, filename, 47, 61)
    if language == 'German':
        st.session_state.practice_language = "de-DE"
        st.session_state.speaker = "de-DE-Standard-B"
        phrase = selectLang(df, content, filename, 62,76)
    if language == 'Japanese':
        st.session_state.practice_language = "ja-JP"
        st.session_state.speaker = "ja-JP-Standard-A"
        phrase = selectLang(df, content, filename, 97,116)
    if language == 'Russian':
        st.session_state.practice_language = "ru-RU"
        st.session_state.speaker = "ru-RU-Standard-A"
        phrase = selectLang(df, content, filename, 77,96)
    
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(phrase)
    
    return phrase

def main():
    filename = 'prevPhrase.txt'
    content = ''

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'languagePhrases.csv')
    df = pd.read_csv(file_path, on_bad_lines='skip')

    phraseText = ""

    st.title("Linguistify.")
    st.text("Master your speech.")

    if 'user_language' not in st.session_state:
        st.session_state.user_language = "English"  # Default language

    if 'practice_language' not in st.session_state:
        st.session_state.practice_language = "en-US"  # Default language
        selectLang(df, content, filename, 32, 46)

    user_language = st.selectbox(
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

    practice_language = st.selectbox(
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

    st.session_state.user_language = user_language

    phrase = practiceSwitchCase(df, content, filename, practice_language)
    
    st.write(f'Now say: "{phrase}"')

    audio_bytes = audio_recorder()

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        wav_file = "audio.wav"

        with open(wav_file, "wb") as f:
            f.write(audio_bytes)

        st.success(f"recording saved")

        if phrase and st.session_state.user_language and st.session_state.practice_language:
            result = getAssessment(phrase, st.session_state.user_language, st.session_state.practice_language)
            st.markdown(
                f"""
                <div style="background-color: rgb(61 114 213 / 20%); padding: 10px; border-radius: 5px; opacity: 1;">
                    {result}
                </div>
                """,
                unsafe_allow_html=True
            )

            # text to speech reference
            client = texttospeech.TextToSpeechClient(credentials=creds)

            text = phrase

            # Set up the audio configuration
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                sample_rate_hertz=22050
            )

            # Set up the synthesis input
            input_text = texttospeech.SynthesisInput(text=text)

            # Set up the voice selection
            if st.session_state.practice_language == 'Chinese (Mandarin, Simplified)':
                voice = texttospeech.VoiceSelectionParams(
                    language_code='cmn-CN',
                    name=st.session_state.speaker
                )
            else:
                voice = texttospeech.VoiceSelectionParams(
                    language_code=st.session_state.practice_language,
                    name=st.session_state.speaker
                )

            # Set up the audio response
            response = client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config
            )

            # Save the audio to a file
            with open("reference.mp3", "wb") as audio_file:
                audio_file.write(response.audio_content)
            
            st.markdown(
                f"""
                <div style="background-color: rgb(61 114 213 / 20%); padding: 10px; border-radius: 5px; opacity: 1;">
                    {'Here is what "' + phrase + '" should sound like:'}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.audio("reference.mp3", format="audio/mpeg", loop=False)

if __name__ == '__main__':
    main()