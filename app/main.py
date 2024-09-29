import streamlit as st
from audio_recorder_streamlit import audio_recorder
from assessment import getAssessment
from google.cloud import texttospeech
import google.auth
import google.cloud.secretmanager
import tempfile

secrets = google.cloud.secretmanager.SecretManagerServiceClient()
google_name = 'projects/pronunciation-assessment-2024/secrets/google_credentials/versions/latest'
google_secret = secrets.access_secret_version(name=google_name)
google_payload = google_secret.payload.data.decode("UTF-8")

# Save the JSON secret to a temporary file
with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
    temp_file.write(google_payload)
    temp_file_path = temp_file.name

creds, project = google.auth.load_credentials_from_file(temp_file_path)

def practiceSwitchCase(language):
    if language == 'English':
        st.session_state.practice_language = "en-US"
        st.session_state.phrase = "We are transitioning to the next state."
        st.session_state.speaker = "en-US-Standard-A"
    if language == 'Spanish':
        st.session_state.practice_language = "es-ES"
        st.session_state.phrase = "Donde esta la biblioteca?"
        st.session_state.speaker = "es-ES-Standard-A"
    if language == 'Chinese (Mandarin, Simplified)':
        st.session_state.practice_language = "zh-CN"
        st.session_state.phrase = "很高兴认识你"
        st.session_state.speaker = "cmn-CN-Standard-A"
    if language == 'French':
        st.session_state.practice_language = "fr-FR"
        st.session_state.phrase = "Enchanté mon ami. Parlez-vous anglais?"
        st.session_state.speaker = "fr-FR-Standard-A"
    if language == 'Italian':
        st.session_state.practice_language = "it-IT"
        st.session_state.phrase = "Mi aiuti, per favore?"
        st.session_state.speaker = "it-IT-Standard-C"
    if language == 'German':
        st.session_state.practice_language = "de-DE"
        st.session_state.phrase = "Ich spreche ein wenig Deutsch."
        st.session_state.speaker = "de-DE-Standard-B"
    if language == 'Japanese':
        st.session_state.practice_language = "ja-JP"
        st.session_state.phrase = "おはようございます"
        st.session_state.speaker = "ja-JP-Standard-A"
    if language == 'Russian':
        st.session_state.practice_language = "ru-RU"
        st.session_state.phrase = "Как доехать до вокзала?"
        st.session_state.speaker = "ru-RU-Standard-A"

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
 
            text = st.session_state.phrase

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
                    {'"' + st.session_state.phrase + '":'}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.audio("reference.mp3", format="audio/mpeg", loop=False)

if __name__ == '__main__':
    main()