"""
this program is the main part of our Voice Assistant, while the program is running, our Voice Assistant is listening to the
voice commands that we give, its functionality is limited to the functions that we have created for it to perform
there is always room for adding new and more interactive features for the program
"""

"""
Contributions:
Estephanos - Weather Scrapping, Where is, and Meaning of words functionality
Srijal - Working on changing pitch of the voice, Quote of the day
Kashav - Building the Voice Assistant, and remaining functionalities
"""

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
#import wolframalpha
#import ecapture as ec
from requests_futures.sessions import FuturesSession
import json
import re
from pprint import pprint
from HTMLParser import HTMLParser
import re
import sys
import numpy as np
import soundfile as sf
import librosa
from bs4 import BeautifulSoup



listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) #id 1 represents female voice, id 0 represents male voice


"""
this function is used for the voice assistant to talk
it uses text to speech to work properly
does not return anything
"""
def talk(text):
    engine.say(text)
    engine.runAndWait()



"""
this function is used to take command from the user
whenever the function is called, it will start listening, convert speech to text,
replaces the wakeword with a blank space
if the wake word is detected in the command, the string with the command is return,
else none is returned 
"""
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


"""
this function is the conditional function of the virtual assistant where all the conditions
for each command is provided.
"""
def run_alexa(command):

    print(command)

    if 'play' in command: #plays any song or video on youtube
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)


    elif 'who are you' in command: #ask alexa about itself
        talk("I am Alexa, your personal voice assistant or something like that, I don't really know yet.")


    elif 'time' in command: #ask about time
        timer = datetime.datetime.now().strftime('%I:%M %p')
        print(timer)
        talk("The current time is" + timer)


    elif 'who is' in command: #ask who a person or a name is
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk("According to Wikipedia,")
        print(info)
        talk(info)


    elif 'open wikipedia' in command: #open wikipedia
        webbrowser.open_new_tab("https://en.wikipedia.org/wiki/Main_Page")
        talk("Opening Wikipedia")
        time.sleep(5)


    elif 'wikipedia' in command: #open wikipedia to search any info
        talk('Searching wikipedia...')
        command = command.replace("wikipedia","")
        info = wikipedia.summary(command, sentences=2)
        talk("According to Wikipedia,")
        print(info)
        talk(info)


    elif 'joke' in command: #alexa tells you a joke
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)


    elif 'open youtube' in command: #opens youtube
        webbrowser.open_new_tab("https://www.youtube.com")
        talk("Opening YouTube")
        time.sleep(5)


    elif 'open gmail' in command: #opens your gmail if logged in
        webbrowser.open_new_tab("https://www.gmail.com")
        talk("Opening Gmail")
        time.sleep(5)


    elif 'open google' in command: #opens google search page
        webbrowser.open_new_tab("https://www.google.com")
        talk("Opening Google")
        time.sleep(5)


    elif 'open calendar' in command: #opens google calendar if logged in
        webbrowser.open_new_tab("https://calendar.google.com")
        talk("Opening your calendar")
        time.sleep(5)


    elif 'where is' in command: #tells you where a place is
        print('..')
        words = command.split('where is')
        print(words[-1])
        link = str(words[-1])
        link = re.sub(' ', '', link)
        talk('Locating')
        time.sleep(2)
        talk(link)
        time.sleep(4)
        link = f'https://www.google.co.in/maps/place/{link}'
        print(link)
        webbrowser.open(link)


    elif 'meaning' in command: #tells you the meaning of a word
        print('..')
        words = command.split(' ')
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



    elif 'weather' in command: #tells you what the weather is in your location
        print('..')
        words = command.split('in')
        print(words[-1])
        scrape_weather(words[-1])


    elif 'stop' in command: # tells alexa to stop talking, alexa shuts down
        return

    #work on the day
    #fact of the day
    #this day in history



    elif 'quote' in command: # gives you a quote
        r = get_quotes(num=1)
        val = extract_quote(r)
        print(val)
        talk(val)


"""
Supporting function for the conditions above
"""

def extract_quote(text): #supports the condition that gives you  a quote
    #text = text[:-3]
    text.replace("document.write('", "")
    text.replace(".'); document.write('More quotes ", "")
    return text


def get_quotes(num): #supports the condition that gives you  a quote
    url = "http://www.quotedb.com/quote/quote.php?action=random_quote"
    session = FuturesSession()
    return session.get(url)


def scrape_weather(city): # supports the condition that returns the weather
    url = 'https://www.google.com/search?q=accuweather+' + city
    page = requests.get(url)


    soup = BeautifulSoup(page.text, 'lxml')
    links = [a['href'] for a in soup.findAll('a')]
    link = str(links[16])
    link = link.split('=')
    link = str(link[1]).split('&')
    link = link[0]

    page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'lxml')

    time = soup.find('p', attrs={'class': 'cur-con-weather-card__subtitle'})
    time = re.sub('\n', '', time.text)
    time = re.sub('\t', '', time)
    time = 'Time: ' + time
    temperature = soup.find('div', attrs={'class': 'temp'})
    temperature = 'Temperature: ' + temperature.text

    realfeel = soup.find('div', attrs={'class': 'real-feel'})
    realfeel = re.sub('\n', '', realfeel.text)
    realfeel = re.sub('\t', '', realfeel)
    realfeel = 'RealFeel: ' + realfeel[-3:] + 'C'
    climate = soup.find('span', attrs={'class': 'phrase'})
    climate = "Climate: " + climate.text

    info = 'For more information visit: ' + link

    print('The weather for today is: ')
    print(time)
    print(temperature)
    print(realfeel)
    print(climate)
    print(info)
    talk('The weather for today is: ')
    talk(time)
    talk(temperature)
    talk(realfeel)
    talk(climate)
    talk('For more information visit accuweather.com')
    time.sleep(5)



def show_definitions(soup): # supports the condition that gives you the meaning of the words
    print()
    senseList = []
    senses = soup.find_all('li', class_='sense')
    for s in senses:
        definition = s.find('span', class_='def').text
        talk(definition)
        time.sleep(5)


def sec_command():
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        print(command)
        return command


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()




"""
this part is not completed yet, but it is intended to be used later to change the pitch of the voices

def extract_quote(text):
    matches = re.findall(r'document.write\(\'(.*)\'\)', text)
    if not matches or len(matches) != 2:
        return None
    quote = strip_tags(matches[0])
    author = re.search(r'More quotes from (.*)', strip_tags(matches[1]))
    if author:
        author = author.group(1)
    return (quote, author)

#takes .wav variable and returns a numpy array
def wav_to_numpy_arr(sound):
    return sf.write(sound, testArray, 48000)


#signal = numpy array that is our waveform
#sr  = sample rate
#num_semitone = number of semitones we want to scale the audio up or down the signal. Positive number is going up, negative is going down
def change_pitch(signal, sr, num_semitone):
    return librosa.return.pitch_shift(singal, sr, num_semitone)

"""


"""
this is the main function where the entire program starts
"""
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


