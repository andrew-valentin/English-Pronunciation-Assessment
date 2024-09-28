import os
from groq import Groq
import json
import azure.cognitiveservices.speech as speechsdk

# Groq API Key setup
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Azure Speech SDK setup
speech_key = "409746937a7e4969a8e69fed1f19294f"
service_region = "eastus"
language = "en-US"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)

pronunciation_config = speechsdk.PronunciationAssessmentConfig( 
    reference_text="", 
    grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark, 
    granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme, 
    enable_miscue=False) 
pronunciation_config.enable_prosody_assessment() 
pronunciation_config.enable_content_assessment_with_topic("greeting")
pronunciation_config.apply_to(speech_recognizer)

# Start recognition
print('Say something...')
result = speech_recognizer.recognize_once()
print('done.')

# Extract pronunciation assessment result
pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(result)
pronunciation_assessment_result_json = result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
pronunciation_assessment_result_data = json.loads(pronunciation_assessment_result_json)

sentence = pronunciation_assessment_result_data['NBest'][0]['Lexical']
accuracy_overall = pronunciation_assessment_result_data['NBest'][0]['PronunciationAssessment']['AccuracyScore']
words = pronunciation_assessment_result_data['NBest'][0]['Words']

# Log the sentence and score
print(f"Sentence: {sentence}")
print(f"Overall Pronunciation Score: {accuracy_overall}")
for word in words:
    print(word['Word'], ':', word['PronunciationAssessment']['AccuracyScore'])

# Function to get pronunciation score analysis from Groq API
def get_pronunciation_score(theScore, model, sentence, words):
    word_scores = "\n".join([f"{word['Word']}: {word['PronunciationAssessment']['AccuracyScore']}" for word in words])

    messages = [
        {
            "role": "system",
            "content": "You are a linguistic professor that helps the user become more fluent in the English language. 0 is a very bad pronunciation. 100 is a very good pronunciation. Anything below 50 means it needs pronunciation improvement."
        },
        {
            "role": "user",
            "content": f"Sentence: {sentence}\n\nWord Scores:\n{word_scores}\n\nOverall Score: {theScore}\n\nPrompt: Analyze the score {theScore} and provide feedback on how to improve pronunciation for the sentence."
        }
    ]

    result = client.chat.completions.create(model=model, messages=messages, temperature=0.7, max_tokens=1200)
    return result

# Replace input with the Azure accuracy score
theScore = accuracy_overall
result = get_pronunciation_score(theScore, "llama-3.1-70b-versatile", sentence, words)
result_content = result.choices[0].message.content

# Print the Groq comment analysis
print(result_content)
