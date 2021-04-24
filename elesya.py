import os, sys, subprocess, psutil
from time import sleep
import random
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup as BS
import requests, bs4, re
import webbrowser as wb
import pyautogui as pg
import cv2
from selenium import webdriver
# from face import main
from subprocess import call
import requests, bs4, re, webbrowser
import os, sys, subprocess
from urllib import request
from urllib.parse import quote
import urllib.request
import html2text


# настройки
opts = {
    "alias": ('елес', 'елеся', 'и леся', 'леся', 'илеся', 'еся','елец','олеся',
              'элисия','елисе','elisey','элеси','жилище','элисед','elisio','elise',
              'жилища','ереси','элисис','делисия','гилея','илюся','элез',"железо"),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси','найди','найти',
            'сделай','включи'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "open_browse": ('открой браузер', 'открой гугл', 'открой интернет'),
        "close_browse": ('закрой браузер', 'закрой гугл', 'закрой интернет'),
        "off_comp":('перезагрузи комп', 'перезагрузи компьютер', 'перезагрузка'),
        "weather_w": ('погода','какая погода'),
        'funny': ('анекдот','расскажи анекдот','рассмеши меня', 'ты знаешь анекдоты'),
        "whome": ('Кто я', 'твой создатель'),
        "search_youtube":("ютюб",'утуб','ютуб','youtube'),
        "screen": ('скрин',"скриншот","фото"),
        "search": ('искать','поисковик','поиск'),
        "search_pic": ('картинка','картинку','изображение'),
        "new_tab": ('новую вкладку', 'новая вкладка', 'вкладка','вкладку'),
        "close_tab": ('закрой вкладку','закрыть вкладку'),
        "hello": ('привет', 'здравствуй'),
        'camera': ('камера','видеокамера'),
        "open_notebook": ("блокнот","запись"),
        "open_calc": ("калькулятор","считать"),
        'close_note_book': ("закрой блокнот", "закрой"),
        "open_telegram": ("открой telegram","открой телеграм","телега","открой телегу"),
        "close_telegram": ("закрой telegram","закрой телеграм","закрой телегу")
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
            # обращаются к Елесе
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            if len(cmd.split())>1:
                user_word = cmd.split(' ', 1)[1]
            else:
                user_word =cmd
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'],user_word)

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

# Запускает внешнюю команду ОС
def osrun(cmd):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)

def execute_cmd(cmd,user_word):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak(f"Сейчас {now.hour} часов {now.minute} минут")

    elif cmd == "search_youtube":
        print(user_word)
        b = user_word.split()
        b = '+'.join(b)
        zz = []
        sq = 'http://www.youtube.com/results?search_query=' + quote(b)
        doc = urllib.request.urlopen(sq).read().decode('cp1251', errors='ignore')
        match = re.findall("\?v\=(.+?)\"", doc)
        if not (match is None):
            for ii in match:
                if (len(ii) < 25):
                    zz.append(ii)
        zz2 = dict(zip(zz, zz)).values()
        zz3 = []
        for qq in zz2: zz3.append(qq)
        s = zz3[0]
        print(s)
        s = 'https://www.youtube.com/watch?v=' + s + '?autoplay=1'
        wb.open(s)
        speak(f"Запрос {user_word} найден")


    elif cmd == "open_notebook":
        speak("открываю ваш блокнот")
        osrun('notepad')


    elif cmd == "open_calc":
        speak("открываю калькулятор")
        osrun('calc')

    elif cmd == "open_telegram":
        speak("открываю телеграм")
        os.startfile(r"C:\Users\ivane\AppData\Roaming\Telegram Desktop\Telegram.exe")
    elif cmd == "close_telegram":
        speak("закрываю телеграм")
        for process in (process for process in psutil.process_iter() if process.name() == "Telegram.exe"):
            process.kill()



    elif cmd == 'open_browse':
        try:
            wb.open("https://www.google.ru/")
            speak("Браузер открыт")

        except TypeError as e:
            speak("У Елеси не вышло, видно руки из гнезна растут")

    elif cmd == "new_tab":
        try:
            pg.FAILSAFE = False
            x, y = pg.locateCenterOnScreen(r"C:\Users\ivane\eles\elesya_voice_hub\photo\tab_open.png")
            pg.click(x, y)
            pg.move(50, 50, 0.5)
            speak("Новая вкладка открыта")
        except TypeError as e:
            speak("У Елеси не вышло, видно руки из гнезна растут")

    elif cmd == 'close_tab':
        try:
            pg.FAILSAFE = False
            x, y = pg.locateCenterOnScreen(r"C:\Users\ivane\eles\elesya_voice_hub\photo\tab_close.png")
            pg.click(x, y)
            pg.move(50, 50, 0.5)
            speak("Вкладка закрыта")
        except TypeError as e:
            speak("У Елеси не вышло, видно руки из гнезна растут")

    elif cmd == 'close_browse':
        try:
            pg.FAILSAFE = False
            x,y = pg.locateCenterOnScreen(r"C:\Users\ivane\eles\elesya_voice_hub\photo\browser_close.png")
            pg.click(x,y)
            speak("Браузер закрыт")
        except TypeError as e:
            speak("У Елеси не вышло, видно руки из гнезна растут")


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
        speak("Вы лучший в мире человек, мой создатель Иван Елескин, ваша мудрость несравненна")


    elif cmd == "search":
        b = user_word.split()
        b = '+'.join(b)
        wb.open(f"https://www.google.com/search?q={b}&rlz=1C1CHZN_ruEE949EE949&oq=%D0%B3%D0%B4%D0%B5+%D0%B6%D0%B8%D0%B2%D1%83%D1%82+%D0%BA%D0%B8%D1%82%D1%8B&aqs=chrome..69i57j0l2j0i22i30l7.5522j0j15&sourceid=chrome&ie=UTF-8")

    elif cmd == "search_pic":
        b = user_word.split()
        b = '+'.join(b)
        wb.open(f"https://www.google.com/search?q={b}&tbm=isch&ved=2ahUKEwj5gZ_Oq5LwAhWXsSoKHUUVBUwQ2-cCegQIABAA&oq=%D0%BA%D0%B8%D1%82&gs_lcp=CgNpbWcQAzIECAAQQzIECAAQQzIECAAQQzIECAAQQzICCAAyAggAMgIIADICCAAyAggAMgIIADoGCAAQBxAeOgQIABAYUNQhWM1AYNJCaABwAHgAgAGmAYgB-giSAQM3LjSYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=gq2BYPm4C5fjqgHFqpTgBA&bih=937&biw=1920&rlz=1C1CHZN_ruEE949EE949")


    elif cmd == "screen":
        now = datetime.datetime.now()
        pg.screenshot(rf"C:\Users\ivane\eles\elesya_voice_hub\screen\{now.minute}.png")
        speak("Скрин сделан")

    elif cmd == "hello":
        tmp = ['хэлоу', 'привет', 'салам', 'здравствуйте', 'тэрэ','бонжур']
        num = random.choice(tmp)
        speak(num)


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


speak("Добрый день. Меня зовут Елеся")
# cap = cv2.VideoCapture(0)
#
# while True:
#     speak("Начинаю индентификацию")
#     ret, img = cap.read()
#     cv2.imshow("camera", img)
#     pg.hotkey("escape")
#     if cv2.waitKey(10) == 27:
#         pg.screenshot(rf"C:\Users\ivane\eles\elesya_voice_hub\photo\access.png")
#         speak("Лицо отсканировано")
#         access = main()
#         if access[0] == True:
#             speak(access[1])
#             break
#         elif access[0] == False:
#             speak(access[1])
# cap.release()
# cv2.destroyAllWindows()


while True:
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    with m as source:
        audio = r.listen(source)
    callback(r, audio)
    time.sleep(0.1)

