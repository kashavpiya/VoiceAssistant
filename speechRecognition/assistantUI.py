from tkinter import *
import numpy as np
import PIL.Image, PIL.ImageTk
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import pyowm
from PIL import Image
import requests
import pyaudio
import pywhatkit
import pyjokes
import time
import json
import re
import argparse
from bs4 import BeautifulSoup

a = {"Kashav Piya": "kashavpiya19@augustana.edu"}
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # id 1 represents female voice, if id set to 0 we get a male voice

window = Tk()

global dummy
global dummy1

dummy = StringVar()
dummy1 = StringVar()


def talk(command):
    engine.say(command)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        dummy.set("Good Morning Sir")
        window.update()
        talk("Good Morning Sir!")
    elif 12 <= hour <= 18:
        dummy.set("Good Afternoon Sir!")
        window.update()
        talk("Good Afternoon Sir!")
    else:
        dummy.set("Good Evening Sir")
        window.update()
        talk("Good Evening Sir!")
    talk("Greetings, I am Summer, your personal voice assistant.")


def show_definitions(soup):
    print()
    senseList = []
    senses = soup.find_all('li', class_='sense')
    num = 0
    for s in senses:
        if num == 1:
            pass
        definition = s.find('span', class_='def').text
        talk(definition)
        time.sleep(5)
        num = 1
    num = 0


def takeCommand():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        dummy.set("Listening...")
        window.update()
        print("Listening...")
        listener.pause_threshold = 1
        listener.energy_threshold = 400
        audio = listener.listen(source)
    try:
        dummy.set("Recognizing...")
        window.update()
        print("Recognizing")
        query = listener.recognize_google(audio, language='en-us')
    except Exception as e:
        return "None"
    dummy1.set(query)
    window.update()
    return query


def get_location():
    """ Function To Print GeoIP Latitude & Longitude """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' + my_ip + '.json')
    geo_data = geo_request.json()
    geo = geo_data['city']
    return geo


def play():
    btn2['state'] = 'disabled'
    btn0['state'] = 'disabled'
    btn1.configure(bg='orange')
    wishme()
    while True:
        btn1.configure(bg='orange')
        city = get_location()
        window.update()
        query = takeCommand().lower()
        if 'exit' in query:
            dummy.set("Personal Voice Assistant Shutting Down")
            btn1.configure(bg='#5C85FB')
            btn2['state'] = 'normal'
            btn0['state'] = 'normal'
            window.update()
            talk("Personal Voice Assistant Shutting Down")
            break

        elif 'wikipedia' in query:
            if 'open wikipedia' in query:
                webbrowser.open('wikipedia.com')
            else:
                try:
                    talk("searching wikipedia")
                    query = query.replace("according to wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    talk("According to wikipedia")
                    dummy.set(query)
                    window.update()
                    talk(results)
                except Exception as e:
                    dummy.set('Sorry, I could not find any results')
                    window.update()
                    talk('Sorry, I could not find any results')

        elif 'open google' in query:
            dummy.set('opening google')
            window.update()
            talk('opening google')
            webbrowser.open("google.com")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            dummy.set(joke)
            talk(joke)

        elif 'meaning' in query:
            print('..')
            words = query.split(' ')
            word = words[-1]
            scrape_url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word
            print(words[-1])
            headers = {"User-Agent": ""}
            web_response = requests.get(scrape_url, headers=headers)

            if web_response.status_code == 200:
                soup = BeautifulSoup(web_response.text, 'html.parser')

                try:
                    # show_origin(soup)
                    show_definitions(soup)
                except AttributeError:
                    talk('Word not found!!')
            else:
                talk('Failed to get response...')

        elif 'open calendar' in query:
            dummy.set("Opening Calendar")
            webbrowser.open_new_tab("https://calendar.google.com")
            talk("Opening your calendar")
            time.sleep(5)

        elif 'open gmail' in query:
            dummy.set("Opening Gmail")
            webbrowser.open_new_tab("https://www.gmail.com")
            talk("Opening Gmail")
            time.sleep(5)

        elif 'open youtube' in query:
            dummy.set("Opening YouTube")
            webbrowser.open_new_tab("https://www.youtube.com")
            talk("Opening YouTube")
            time.sleep(5)

        elif 'say hello' in query or 'who are you' in query:
            dummy.set("I am Summer, your personal voice assistant or something like that, I don't really know yet.")
            window.update()
            talk("I am Summer, your personal voice assistant or something like that, I don't really know yet.")

        elif 'hello' in query:
            dummy.set("I am Summer, your personal voice assistant or something like that, I don't really know yet.")
            window.update()
            talk("I am Summer, your personal voice assistant or something like that, I don't really know yet.")

        elif 'open stackoverflow' in query:
            dummy.set('Opening stackoverflow')
            window.update()
            talk('opening stackoverflow')
            webbrowser.open('stackoverflow.com')

        elif 'play' in query:
            song = query.replace('play', '')
            dummy.set('Playing' + song)
            talk('playing' + song)
            pywhatkit.playonyt(song)

        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            dummy.set("Sir the time is %s" % strtime)
            window.update()
            talk("Sir the time is %s" % strtime)

        elif 'the date' in query:
            strdate = datetime.datetime.today().strftime("%d %m %y")
            dummy.set("Sir today's date is %s" % strdate)
            window.update()
            talk("Sir today's date is %s" % strdate)

        elif 'weather' in query:
            owm = pyowm.OWM('api-key')  # open weather map API key
            # current weather forecast
            loc = owm.weather_at_place(city)
            weather = loc.get_weather()
            # status
            status = weather.get_detailed_status()
            dummy.set(f'{status} in {city}')
            window.update()
            talk(f'{status} in {city}')
            # temperature
            temp = weather.get_temperature(unit='celsius')
            for key, val in temp.items():
                if key == 'temp':
                    dummy.set(f'{val} degree celcius')
                    window.update()
                    talk(f"current temperature is {val} degree celcius")
            # humidity, wind, rain, snow
            humidity = weather.get_humidity()
            wind = weather.get_wind()
            dummy.set(f'{humidity} grams per cubic meter')
            window.update()
            talk(f'humidity is {humidity} grams per cubic meter')
            dummy.set(f'wind {wind}')
            window.update()
            talk(f'wind {wind}')
            # sun rise and sun set
            sr = weather.get_sunrise_time(timeformat='iso')
            ss = weather.get_sunset_time(timeformat='iso')
            dummy.set(sr)
            window.update()
            talk(f'SunRise time is {sr}')
            dummy.set(ss)
            window.update()
            talk(f'SunSet time is {ss}')
            # clouds and rain
            loc = owm.three_hours_forecast(city)
            clouds = str(loc.will_have_clouds())
            rain = str(loc.will_have_rain())
            if clouds == 'True':
                dummy.set("It may have clouds in next 5 days")
                window.update()
                talk("It may have clouds in next 5 days")
            else:
                dummy.set("It may not have clouds in next 5 days")
                window.update()
                talk("It may not have clouds in next 5 days")
            if rain == 'True':
                dummy.set("It may rain in next 5 days")
                window.update()
                talk("It may rain in next 5 days")
            else:
                dummy.set("It may not rain in next 5 days")
                window.update()
                talk("It may not rain in next 5 days")


def update(ind):
    frame = frames[ind % 100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)


label2 = Label(window, textvariable=dummy1, bg='#FAB60C')
label2.config(font=("Courier", 20))
dummy1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable=dummy, bg='#ADD8E6')
label1.config(font=("Courier", 20))
dummy = ('Welcome')
label1.pack()

frames = [PhotoImage(file='assist.gif', format='gif -index %i' % (i)) for i in range(100)]
window.title('Summer')

label = Label(window, width=500, height=500)
label.pack()
window.after(0, update, 0)

btn0 = Button(text='WISH ME', width=20, command=wishme, bg='#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text='START', width=20, command=play, bg='#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text='EXIT', width=20, command=window.destroy, bg='#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()

window.mainloop()
