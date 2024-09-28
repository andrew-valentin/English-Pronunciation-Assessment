const sdk = require("microsoft-cognitiveservices-speech-sdk");
const speech_key = "409746937a7e4969a8e69fed1f19294f"
const service_region = "eastus"
const language = "en-US"

function getAssessment(phrase)
{
    const speechConfig = new sdk.SpeechConfig(speech_key, service_region);
    speechConfig.speechRecognitionLanguage = language;

    var pronunciationAssessmentConfig = new sdk.PronunciationAssessmentConfig( 
        referenceText: "", 
        gradingSystem: sdk.PronunciationAssessmentGradingSystem.HundredMark,  
        granularity: sdk.PronunciationAssessmentGranularity.Phoneme,  
        enableMiscue: false); 
    pronunciationAssessmentConfig.enableProsodyAssessment(); 
    pronunciationAssessmentConfig.enableContentAssessmentWithTopic("greeting");

    const speechRecognizer = new sdk.SpeechRecognizer(speechConfig);
    speechRecognizer.audioConfig = new sdk.AudioConfig({ useDefaultMicrophone: true });

    speechRecognizer.recognizeOnceAsync().then(result => {
        console.log(result.text);
    }).catch(error => {
        console.error(error);
    });
}

getAssessment('hello. how are you today?')