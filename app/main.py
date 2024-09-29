import streamlit as st
from audio_recorder_streamlit import audio_recorder
from assessment import getAssessment

def practiceSwitchCase(language):
    if language == 'English':
        st.session_state.practice_language = "en-US"
        st.session_state.phrase = "We are transitioning to the next state."
    if language == 'Spanish':
        st.session_state.practice_language = "es-ES"
        st.session_state.phrase = "Donde esta la biblioteca?"
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

def main():
    st.title("Linguistify.")
    st.text("Master your speech.")

    if 'user_language' not in st.session_state:
        st.session_state.user_language = "English"  # Default language

    if 'practice_language' not in st.session_state:
        st.session_state.practice_language = "en-US"  # Default language
        st.session_state.phrase = "We are transitioning to the next state."

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
    practiceSwitchCase(practice_language)

    st.write(f"Selected Language: {st.session_state.practice_language}")
    st.write(f"Now say: {st.session_state.phrase}")

    audio_bytes = audio_recorder()

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

        wav_file = "audio.wav"

        with open(wav_file, "wb") as f:
            f.write(audio_bytes)

        st.success(f"recording saved")

        if st.session_state.phrase and st.session_state.user_language and st.session_state.practice_language:
            result = getAssessment(st.session_state.phrase, st.session_state.user_language, st.session_state.practice_language)
            st.write(result)

if __name__ == '__main__':
    main()