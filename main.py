import webbrowser
import speech_recognition as sr
import pyttsx3
import pyaudio
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import requests
import json
import wolframalpha
import ecapture as ec

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #id 1 represents female voice, id 0 represents male voice


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
            else:
                return "None"


    except Exception as e:
        talk("Pardon me, please say that again")
        return "None"

    return command


def run_alexa(command):
    # command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'who are you' in command:
        talk("I am Alexa, your personal voice assistant or something like that, I don't really know yet.")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk("The current time is" + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk("According to Wikipedia,")
        print(info)
        talk(info)
    elif 'wikipedia' in command:
        talk('Searching wikipedia...')
        command = command.replace("wikipedia","")
        info = wikipedia.summary(command, sentences=2)
        talk("According to Wikipedia,")
        print(info)
        talk(info)
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
    elif 'open youtube' in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        talk("Opening YouTube")
        time.sleep(5)
    elif 'open gmail' in command:
        webbrowser.open_new_tab("https://www.gmail.com")
        talk("Opening Gmail")
        time.sleep(5)
    elif 'open google' in command:
        webbrowser.open_new_tab("https://www.google.com")
        talk("Opening Google")
        time.sleep(5)
    elif 'open calendar' in command:
        webbrowser.open_new_tab("https://calendar.google.com")
        talk("Opening your calendar")
        time.sleep(5)
    elif 'weather' in command: #not working yet, figuring it out (gives invalid API key error)
        api_key = "#################"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        talk("What is the name of your city?")
        city = sec_command()
        complete_url = base_url + "appid ="+api_key+"&q=" + city
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            print(x)
            y = x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            talk(" Temperature in kelvin unit is " +
                  str(current_temperature) +
                  "\n humidity in percentage is " +
                  str(current_humidiy) +
                  "\n description  " +
                  str(weather_description))
            print(" Temperature in kelvin unit = " +
                  str(current_temperature) +
                  "\n humidity (in percentage) = " +
                  str(current_humidiy) +
                  "\n description = " +
                  str(weather_description))
    elif "camera" in command or "take a photo" in command:
        ec.capture(0, "robo camera", "img.jpg")

    elif 'stop' in command:
        return


def sec_command():
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        print(command)
        return command

if __name__ == '__main__':
    talk("Greetings, I am your personal voice assistant.")
    while True:
        talk("Tell me how can I help you?")
        statement = take_command().lower()
        if statement == 0:
            continue
        elif 'stop' in statement or 'bye' in statement or 'exit' in statement:
            talk("Personal Voice Assistant Shutting Down")
            exit()
        else:
            run_alexa(statement)
        time.sleep(2)
