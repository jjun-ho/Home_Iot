import speech_recognition as sr  #음성 인식
from gtts import gTTS  #Google Text To Speech
import os
import time #시간 저장
import playsound #mp3파일 재생
import pandas as pd #pandas -> DataFrame -> excel 형식 변환
from pandas import DataFrame
import pymysql #mysql

"""
data = {
    '목적': ['불', '온도', '습도', '커튼', '창문'],
    '동작': ['켜', '꺼', '알려', '열어', '닫아'],
    '어미': ['줘', 'NaN', 'NaN', 'NaN', 'NaN' ]
}
df = pd.DataFrame(data)
"""

#mysql id/pass
my_id = "han"
my_pass = "980704"

#현재시간을 저장하는 변수
timer = " "
timer = time.strftime('%Y.%m.%d %I:%M:%S %p', time.localtime(time.time()))

#변수 선언
global javis
javis = False
case = 0

def speak(text): #javis의 대답
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_audio_main(): #실행 문장 음성 인식
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

def get_audio(): #자비스 호출 문장 음성 인식
    global javis
    javis = False
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=0, phrase_time_limit=1.8)
        said = " "
        try:
            said = r.recognize_google(audio, language='ko-KR')
            if(said == "자비스"):
                javis = True
                speak("네")
                said = get_audio_main()
            else:
                javis = False
                said = " "
                print("Please Again1")
        except Exception as e:
            print("Exception: " + str(e))
            javis = False
            said = " "
            print("Please Again2")
    return said

# pandas/ 열 목록만 있는 빈 excel 파일 생성
df = DataFrame({
    '시간': [0],
    '목적': [0],
    '동작': [0],
    '어미': [0],
    'case': [0]
})
df.to_excel('iot.xlsx')

#main
speak("안녕하세요 자비스입니다")

while True:
    while (javis == False):
        s_text = get_audio()
        if(javis == True):
            break
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

    # excel
    df2 = pd.read_excel("iot.xlsx", engine="openpyxl", index_col=0)
    new = {'시간': timer, '목적': object, '동작': motion, '어미': ending, 'case': case}
    df3 = df2.append(new, ignore_index=True)
    df3.to_excel('iot.xlsx')

    #mysql
    db = pymysql.connect(host="localhost", user=my_id, password=my_pass, charset="utf8")
    cursor = db.cursor()
    cursor.execute('USE homedb')
    sql = "INSERT INTO `iot`(task) VALUES (%s);"
    cursor.execute(sql, case)
    db.commit()
    db.close()

    #변수 초기화
    object = " "
    motion = " "
    ending = " "
    case = 0
    javis = False
    speak("넵") ##실행완료를 알림
