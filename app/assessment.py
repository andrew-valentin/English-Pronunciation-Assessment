import os
from groq import Groq
import json
import azure.cognitiveservices.speech as speechsdk
import google.cloud.secretmanager

secrets = google.cloud.secretmanager.SecretManagerServiceClient()

# Groq API Key setup
groq_name = 'projects/pronunciation-assessment-2024/secrets/groq_api_key/versions/latest'
groq_secret = secrets.access_secret_version(name=groq_name)
groq_payload = groq_secret.payload.data.decode("UTF-8")
client = Groq(api_key=groq_payload)

# Azure Speech SDK setup
service_region = "eastus"

# Function to get pronunciation score analysis from Groq API
def get_pronunciation_score(theScore, model, sentence, word_scores, user_lang, practice_lang):
    if practice_lang == 'en-US':
        language = 'English'
    if practice_lang == 'es-ES':
        language = 'Spanish'
    if practice_lang == 'zh-CN':
        language = 'Chinese (Mandarin, Simplified)'
    if practice_lang == 'fr-FR':
        language = 'French'
    if practice_lang == 'it-IT':
        language = 'Italian'
    if practice_lang == 'de-DE':
        language = 'German'
    if practice_lang == 'ja-JP':
        language = 'Japanese'
    if practice_lang == 'ru-RU':
        language = 'Russian'

    messages = [
        {
            "role": "system",
            "content": "You are a linguistic professor that helps the user become more fluent in the " + language + " language. 0 is a very bad pronunciation. 100 is a very good pronunciation. Anything below 50 means it needs pronunciation improvement. Also seperate this output as one section for results and another for tips"
        },
        {
            "role": "user",
            "content": f"Sentence: {sentence}\n\nWord Scores:\n{word_scores}\n\nOverall Score: {theScore}\n\nPrompt: Analyze the score {theScore} and provide feedback in " + user_lang + " on how to improve pronunciation for the sentence."
        }
    ]

    result = client.chat.completions.create(model=model, messages=messages, temperature=0.7, max_tokens=1200)
    return result

def getAssessment(phrase, user_lang, practice_lang):
    speech_name = 'projects/pronunciation-assessment-2024/secrets/speech_key/versions/latest'
    speech_secret = secrets.access_secret_version(name=speech_name)
    speech_payload = speech_secret.payload.data.decode("UTF-8")
    speech_config = speechsdk.SpeechConfig(subscription=speech_payload, region=service_region)
    speech_config.speech_recognition_language = practice_lang
    audio_config = speechsdk.AudioConfig(filename='audio.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=practice_lang, audio_config=audio_config)

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
    result = get_pronunciation_score(accuracy_overall, "llama-3.1-70b-versatile", sentence, word_scores, user_lang, practice_lang)
    return result.choices[0].message.content