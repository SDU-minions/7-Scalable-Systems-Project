#PyAudio
#SpeechRecognition
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source)
    print("Time over, thanks")
    
    try:
        res = r.recognize_google(audio_text)
        print("Text: " + res)
    except:
         print("Sorry, I did not get that")