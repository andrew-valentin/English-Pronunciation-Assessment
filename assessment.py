import os
from groq import Groq
import json
import azure.cognitiveservices.speech as speechsdk
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import wave

# Groq API Key setup
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Azure Speech SDK setup
speech_key = "409746937a7e4969a8e69fed1f19294f"
service_region = "eastus"
language = "en-US" #en-US or es-ES
phrase = "Hello, how are you?"

# Function to get pronunciation score analysis from Groq API
def get_pronunciation_score(theScore, model, sentence, word_scores, language):
    if language == 'en-US':
        language = 'English'
    else:
        language = 'Spanish'
    messages = [
        {
            "role": "system",
            "content": "You are a linguistic professor that helps the user become more fluent in the " + language + " language. 0 is a very bad pronunciation. 100 is a very good pronunciation. Anything below 50 means it needs pronunciation improvement."
        },
        {
            "role": "user",
            "content": f"Sentence: {sentence}\n\nWord Scores:\n{word_scores}\n\nOverall Score: {theScore}\n\nPrompt: Analyze the score {theScore} and provide feedback on how to improve pronunciation for the sentence."
        }
    ]

    result = client.chat.completions.create(model=model, messages=messages, temperature=0.7, max_tokens=1200)
    return result

# def getRecording():
#     st.title("Voice recording test")
#
#     audio_bytes = audio_recorder()
#     if audio_bytes:
#         st.audio(audio_bytes, format="audio/wav")
#
#         wav_file = "audio.wav"
#
#         with open(wav_file, "wb")as f:
#             f.write(audio_bytes)
#
#         st.success(f"recording saved")

def getAssessment(phrase, language):

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.AudioConfig(filename='audio.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)

    pronunciation_config = speechsdk.PronunciationAssessmentConfig( 
        reference_text=phrase, 
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark, 
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme, 
        enable_miscue=False) 
    pronunciation_config.enable_prosody_assessment() 
    pronunciation_config.apply_to(speech_recognizer)

    # Open your audio stream
    with open("audio.wav", "rb") as audio_file:
        audio_data = audio_file.read()

    # Send the audio data to the Azure Speech Service
    result = speech_recognizer.recognize_once()

    print("Recognized: {}".format(result.text))
    pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
    print(f"Pronunciation Accuracy: {pronunciation_result.accuracy_score}")
    print(f"Pronunciation Completeness: {pronunciation_result.completeness_score}")
    print(f"Pronunciation Fluency: {pronunciation_result.fluency_score}")
    pronunciation_result.words
    # Extract pronunciation assessment result
    pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(result)
    pronunciation_assessment_result_json = result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
    pronunciation_assessment_result_data = json.loads(pronunciation_assessment_result_json)

    sentence = result.text
    accuracy_overall = pronunciation_result.accuracy_score
    words = pronunciation_result.words
    word_scores = ''

    # Log the sentence and score
    print(f"Sentence: {sentence}")
    print(f"Overall Pronunciation Score: {accuracy_overall}")
    for word in words:
        print(word.word, ':', word.accuracy_score)
        word_scores += str(word.word) + ' : ' + str(word.accuracy_score) + '\n'

    # Replace input with the Azure accuracy score
    result = get_pronunciation_score(accuracy_overall, "llama-3.1-70b-versatile", sentence, word_scores, language)
    return result.choices[0].message.content

# Print the Groq comment analysis
print(getAssessment(phrase, language))