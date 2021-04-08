
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import subprocess
import requests
from bs4 import BeautifulSoup as BS
import requests, bs4, re
import webbrowser as wb
import pyautogui as pg


# настройки
opts = {
    "alias": ('елес', 'елеся', 'и леся', 'леся', 'илеся', 'еся','елец','олеся',
              'элисия','елисе','elisey','элеси','жилище','элисед'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси','найди','найти','открой',
            'сделай'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "open_browse": ('открой браузер', 'открой гугл', 'открой интернет'),
        "close_browse": ('закрой браузер', 'закрой гугл', 'закрой интернет'),
        "off_comp":('перезагрузи комп', 'перезагрузи компьютер', 'перезагрузка'),
        "weather_w": ('погода','какая погода'),
        'funny': ('анекдот','расскажи анекдот','рассмеши меня', 'ты знаешь анекдоты'),
        "whome": ('Кто я', 'твой создатель'),
        "search_youtube":("ютюб",'утуб','ютуб','youtube'),
        "search":("алладин",'аладин', 'aladdin'),
        "screen": ('скрин',"скриншот","фото")
    }
}

# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'open_browse':
        # воспроизвести радио
        # os.system("D:\\Jarvis\\res\\radio_record.m3u")
        subprocess.Popen('C:/Program Files/Google/Chrome/Application/chrome.exe')
        speak("Браузер открыт")

    elif cmd == 'close_browse':
        os.system('TASKKILL /F /IM chrome.exe')
        speak("Браузер закрыт")

    elif cmd == 'off_comp':
        os.system('shutdown -r -t 0')

    elif cmd == 'weather_w':
        r = requests.get(f'https://sinoptik.ua/погода-таллин')
        html = BS(r.content, 'html.parser')

        for el in html.select('#content'):
            t_min = el.select('.temperature .min')[0].text
            t_max = el.select('.temperature .max')[0].text
            text = el.select('.wDescription .description')[0].text
        # f"В Таллине - погода на сегодня:{t_min}, {t_max} {text}")
        speak("В Таллине - погода на сегодня "+ str(t_min) + ":" + str(t_max)+ ":" + str(text))

    elif cmd == 'funny':
        s = requests.get('http://anekdotme.ru/random')
        b = bs4.BeautifulSoup(s.text, "html.parser")
        p = b.select('.anekdot_text')
        s = (p[0].getText().strip())
        reg = re.compile('[^0-9a-zA-Zа-яА-я .,!?-]')
        s = reg.sub('', s)
        speak(s)

    elif cmd == "whome":
        # рассказать анекдот
        speak("Вы лучший в мире человек, мой создатель Иван Елескин, ваша мудрость несравненна")

    elif cmd == "search_youtube":
        wb.open("https://www.youtube.com/")
        speak("Youtube открыт. Пользуйтесь.")

    elif cmd == "search":
        wb.open("https://kadikama.ru/106-aladdin.html")
        speak("Алладин открыт. Приятного просмотра")

    elif cmd == "screen":
        now = datetime.datetime.now()
        img = pg.screenshot(f"{now.minute}.png")
        speak("Скрин сделан")


    else:
        print('Команда не распознана, повторите!')


# запуск

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# # Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', 'ru')

# for voice in voices:
#     if voice.name == 'Aleksandr':
#         speak_engine.setProperty('voice', voice.id)


speak("Добрый день. ")
speak("Меня зовут Елеся")

while True:
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    with m as source:
        audio = r.listen(source)
    callback(r, audio)
    time.sleep(0.1)





