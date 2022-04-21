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

#import for quotes
from bs4 import BeautifulSoup
import pandas as pd
#import requests
import random

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

    # plays any song or video on youtube
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)


    # ask alexa about itself
    elif 'who are you' in command:
        talk("I am Alexa, your personal voice assistant or something like that, I don't really know yet.")


    # ask about time
    elif 'time' in command:
        timer = datetime.datetime.now().strftime('%I:%M %p')
        print(timer)
        talk("The current time is" + timer)


    # ask who a person or a name is
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk("According to Wikipedia,")
        print(info)
        talk(info)


    # open wikipedia
    elif 'open wikipedia' in command:
        webbrowser.open_new_tab("https://en.wikipedia.org/wiki/Main_Page")
        talk("Opening Wikipedia")
        time.sleep(5)


    # open wikipedia to search any info
    elif 'wikipedia' in command:
        talk('Searching wikipedia...')
        command = command.replace("wikipedia","")
        info = wikipedia.summary(command, sentences=2)
        talk("According to Wikipedia,")
        print(info)
        talk(info)


    # alexa tells you a joke
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)


    # opens youtube
    elif 'open youtube' in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        talk("Opening YouTube")
        time.sleep(5)


    # opens your gmail if logged in
    elif 'open gmail' in command:
        webbrowser.open_new_tab("https://www.gmail.com")
        talk("Opening Gmail")
        time.sleep(5)


    # opens google search page
    elif 'open google' in command:
        webbrowser.open_new_tab("https://www.google.com")
        talk("Opening Google")
        time.sleep(5)


    # opens google calendar if logged in
    elif 'open calendar' in command:
        webbrowser.open_new_tab("https://calendar.google.com")
        talk("Opening your calendar")
        time.sleep(5)


    # tells you where a place is
    elif 'where is' in command:
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


    # tells you the meaning of a word
    elif 'meaning' in command:
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



    # tells you what the weather is in your location
    elif 'weather' in command:
        print('..')
        words = command.split('in')
        print(words[-1])
        scrape_weather(words[-1])


    # tells alexa to stop talking, alexa shuts down
    elif 'stop' in command:
        return

    #work on the day
    #fact of the day

    elif 'fact' in command:
        fact = give_fun_fact()
        print(fact)
        talk(fact)
    #this day in history


    # gives you a quote
    elif 'quote' in command:
        authors, quotes = scrape_website(1)
        text = random_quote(quotes, authors)
        print(text)
        talk(text)


"""
Supporting function for the conditions above
"""
# support function for quote to parse quotes from goodreads.com

def scrape_website(page_number):

    #list for the author and quotes
    authors = []
    quotes = []

    # Convert the page numbers to a string and add page number to URL, then make a request to the website
    page_num = str(page_number)
    URL = 'https://www.goodreads.com/quotes/tag/inspirational?page=' + page_num
    webpage = requests.get(URL)

    # Parse the text from the website then get the tag and it's class
    soup = BeautifulSoup(webpage.text, "html.parser")
    quoteText = soup.find_all('div', attrs={'class': 'quoteText'})


    for i in quoteText:
        quote = i.text.strip().split('\n')[0]  # Get the text of the current quote, but only the sentence before a new line
        author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip()

        quotes.append(quote)
        authors.append(author)

    return authors, quotes

# support function to give a random quote from list

def random_quote(quoteList, AuthorList):
    length = len(quoteList)
    num = random.randrange(length - 1)
    return quoteList[num] + " by " + AuthorList[num]

# support function that provides a random useless fun fact

def give_fun_fact():

    url = "https://uselessfacts.jsph.pl/random.json?language=en"

    response = requests.request("GET", url)

    data = json.loads(response.text)

    fact = data['text']

    return fact


# supports the condition that returns the weather
def scrape_weather(city):
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


