import speech_recognition as sr  #음성 인식
from gtts import gTTS  #Google Text To Speech
import os
import time
import playsound #mp3파일 재생
import pandas as pd
import openpyxl
import pymysql
from sqlalchemy import create_engine

my_id = "han"
my_pass = "980704"

timer = " "
timer = time.strftime('%Y.%m.%d %I:%M:%S %p', time.localtime(time.time()))

data = {
    '목적': ['불', '온도', '습도', '커튼', '창문'],
    '동작': ['켜', '꺼', '알려', '열어', '닫아'],
    '어미': ['줘', 'NaN', 'NaN', 'NaN', 'NaN' ]
}
df = pd.DataFrame(data)

case = 0

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

def get_audio_main():
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

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, )
        said =" "
        said = r.recognize_google(audio, language='ko-KR')
        if(said == "자비스"):
            speak("네")
            said = get_audio_main()
            print(said)
        else:
            print("Nothing")
            get_audio()
    return said

speak("안녕하세요 자비스입니다")
s_text = get_audio_main()
s_list = s_text.split()
print(s_list)
object = ""
motion = ""
ending = ""
for word in s_list:
    if "불" in word:
        object = word
    elif "온도" in word:
        object = word
    elif "습도" in word:
        object = word
    elif "커튼" in word:
        object = word
    elif "창문" in word:
        object = word

    elif "켜" in word:
        motion = word
    elif "꺼" in word:
        motion = word
    elif "알려" in word:
        motion = word
    elif "열어" in word:
        motion = word
    elif "닫아" in word:
        motion = word

    elif "줘" in word:
        ending = word

print("object: " + object)
print("motion: " + motion)
print("ending: " + ending)

if (object == "불") & (motion == "켜"):
    case = 1
elif (object == "불") & (motion == "꺼"):
    case = 2
elif (object == "온도") & (motion == "알려"):
    case = 3
elif (object == "습도") & (motion == "알려"):
    case = 4
elif (object == "커튼") & (motion == "열어"):
    case = 5
elif (object == "커튼") & (motion == "닫아"):
    case = 6
elif (object == "창문") & (motion == "열어"):
    case = 7
elif (object == "창문") & (motion == "닫아"):
    case = 8

print("case: " + str(case))

inventors = pd.DataFrame(
    {
    '시간': [timer],
    '목적': [object],
    '동작': [motion],
    '어미': [ending],
    'case': [case]
    })

inventors.to_excel('iot.xlsx')

#mysql

db = pymysql.connect(host="localhost", user=my_id, password=my_pass, charset="utf8")
print(db)
cursor = db.cursor()
cursor.execute('USE homedb')
sql = "INSERT INTO `iot`(task) VALUES (%s);"
cursor.execute(sql, case)
db.commit()
db.close()

