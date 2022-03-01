import webbrowser
import speech_recognition as sr
import pyttsx3
import pyaudio
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time


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
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk("The current time is" + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
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
    elif 'stop' in command:
        return


if __name__ == '__main__':

    while True:
        time.sleep(2)
        talk("Tell me how can I help you?")
        statement = take_command().lower()
        if statement == 0:
            continue
        elif 'stop' in statement:
            talk("Personal Voice Assistant Shutting Down")
            exit()
        else:
            run_alexa(statement)
