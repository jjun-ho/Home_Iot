import speech_recognition as sr  #음성 인식
from gtts import gTTS  #Google Text To Speech
import os
import time
import playsound #mp3파일 재생

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said =" "
        try:
            said = r.recognize_google(audio, language='ko-KR')
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    return said

speak("안녕하세요 자비스입니다")
get_audio()
