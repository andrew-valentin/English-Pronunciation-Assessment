import azure.cognitiveservices.speech as speechsdk
import json

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

# (Optional) get the session ID
speech_recognizer.session_started.connect(lambda evt: print(f"SESSION ID: {evt.session_id}"))

print('Say something...')
result = speech_recognizer.recognize_once()
print('done.')

# The pronunciation assessment result as a Speech SDK object
pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(result)

# The pronunciation assessment result as a JSON string
pronunciation_assessment_result_json = result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
pronunciation_assessment_result_data = json.loads(pronunciation_assessment_result_json)

sentence = pronunciation_assessment_result_data['NBest'][0]['Lexical']
accuracy_overall = pronunciation_assessment_result_data['NBest'][0]['PronunciationAssessment']['AccuracyScore']
words = pronunciation_assessment_result_data['NBest'][0]['Words']

print(sentence, ':', accuracy_overall)
for word in words:
    print(word['Word'], ':', word['PronunciationAssessment']['AccuracyScore'])