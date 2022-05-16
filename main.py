"""
this program is the main part of our Voice Assistant, while the program is running, our Voice Assistant is listening to the
voice commands that we give, its functionality is limited to the functions that we have created for it to perform
there is always room for adding new and more interactive features for the program

Contributions:
Estephanos - Weather Scrapping, Where is, and Meaning of words functionality
Srijal - Working on changing pitch of the voice, Quote of the day, Fact, This day in History
Kashav - Building the Voice Assistant, and remaining functionalities
"""
from email import message
from tkinter import *
from tokenize import String
from PIL import ImageTk, Image
# import pyowm
import webbrowser
import os
from pyparsing import col
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
import re
import random
import argparse
from bs4 import BeautifulSoup

app_string = ["open word", "open powerpoint", "open excel", "open zoom", "open notepad", "open chrome"]
app_link = [r'\Word.lnk', r'\PowerPoint.lnk', r'\Excel.lnk', r'\Zoom.lnk', r'\Notepad.lnk', r'\Google Chrome.lnk']
app_dest = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'

#UI was created through following a codemy video about tkinter and created by ourselves

class Window(Frame):
    def __init__(self, master):
        self.master = master
        master.title("Summer")

        A = Label(master, text="Hi! I am Summer, your voice assistant")
        A.grid(row=0, column=1, columnspan=2)

        clicked = StringVar()
        clicked.set("Functions:")
        dropList = ["Tell time", "Tell Date", "Play Music", "Introduction", "Search Person", "Play Youtube",
                    "Search wiki", "This day info", "Say Fact, Quote, or Joke", "Locate", "Find meaning", "Functions:"]
        drop = OptionMenu(master, clicked, *dropList)
        drop.grid(row=0, column=0)

        # myImg = ImageTk.PhotoImage(Image.open("robot.jpg"))
        # imgLabel = Label(master, image = myImg)
        # imgLabel.grid(row=2, column = 1)

        listenButton = Button(master, text="Listen!", width=25, command=self.Processo_r, fg="yellow", bg="#000000")
        listenButton.grid(row=3, column=1)

        button_quit = Button(master, text="Exit", command=root.quit)
        button_quit.grid(row=3, column=2)

        myLabel2 = Label(master, text="Log:", font=('Helvetica 11 underline'))
        myLabel2.grid(row=4, column=0)

    """
    this function is used for the voice assistant to talk
    it uses text to speech to work properly
    does not return anything
    """

    def talk(self, text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # id 1 represents female voice, id 0 represents male voice
        engine.say(text)
        engine.runAndWait()

    def speech_recog(self):
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=1)

        with mic as s:
            self.talk("How can I help you?")
            audio = r.listen(s, timeout=5)
            r.adjust_for_ambient_noise(s)

        try:
            command = r.recognize_google(audio)
            return command.lower()

        except sr.UnknownValueError:
            self.talk("Please try again, could not understand.")

        except sr.WaitTimeoutError as e:
            self.talk("Please try again")

    def greet(self):
        messages = ["Hi,nice to meet you", "hello", "Nice to meet you", "hey,nice to meet you", "good to meet you!"]
        message = random.choice(messages)
        self.talk(message)

    def tell_time(self):
        localtime = time.asctime(time.localtime(time.time()))
        timer = localtime[11:16]
        self.talk(timer)

    def tell_day(self):
        localtime = time.asctime(time.localtime(time.time()))
        day = localtime[0:3]
        if day == "Sun":
            self.talk("it's sunday")
        if day == "Mon":
            self.talk("it's monday")
        if day == "Tue":
            self.talk("it's tuesday")
        if day == "Wed":
            self.talk("it's wednesday")
        if day == "Thu":
            self.talk("it's thursday")
        if day == "Fri":
            self.talk("it's friday")
        if day == "Sat":
            self.talk("it's saturday")

    def tell_month(self):
        localtime = time.asctime(time.localtime(time.time()))
        month = localtime[4:7]
        if month == "Jan":
            self.talk("it's january")
        if month == "Feb":
            self.talk("it's february")
        if month == "Mar":
            self.talk("it's march")
        if month == "Apr":
            self.talk("it's april")
        if month == "May":
            self.talk("it's may")
        if month == "Jun":
            self.talk("it's june")
        if month == "Jul":
            self.talk("it's july")
        if month == "Aug":
            self.talk("it's august")
        if month == "Sep":
            self.talk("it's september")
        if month == "Oct":
            self.talk("it's october")
        if month == "Nov":
            self.talk("it's november")
        if month == "Dec":
            self.talk("it's december")

    def playMusic(self, command):
        song = command.replace('play', '')
        self.talk('playing' + song)
        pywhatkit.playonyt(song)

    def introduction(self):
        self.talk("I am Summer, your personal voice assistant or something like that, I don't really know yet.")

    def person(self, command):
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        self.talk("According to Wikipedia,")
        self.talk(info)

    def openwiki(self):
        webbrowser.open_new_tab("https://en.wikipedia.org/wiki/Main_Page")
        self.talk("Opening Wikipedia")
        time.sleep(5)

    def openYoutube(self):
        webbrowser.open_new_tab("https://www.youtube.com")
        self.talk("Opening YouTube")
        time.sleep(5)

    def openwikiperson(self, command):
        self.talk('Searching wikipedia...')
        command = command.replace("wikipedia", "")
        info = wikipedia.summary(command, sentences=2)
        self.talk("According to Wikipedia,")
        self.talk(info)

    def jokes(self):
        joke = pyjokes.get_joke()
        self.talk(joke)

    def openGoogle(self):
        webbrowser.open_new_tab("https://www.google.com")
        self.talk("Opening Google")
        time.sleep(5)

    def openCal(self):
        webbrowser.open_new_tab("https://calendar.google.com")
        self.talk("Opening your calendar")
        time.sleep(5)

    def where(self, command):
        words = command.split('where is')
        link = str(words[-1])
        link = re.sub(' ', '', link)
        self.talk('Locating')
        time.sleep(2)
        link = f'https://www.google.co.in/maps/place/{link}'
        webbrowser.open(link)
        time.sleep(5)

    ###

    # function to provide meaning of a word
    # support function to give a random meaning from list

    def show_definitions(self, soup):
        # print()
        senseList = []
        senses = soup.find_all('li', class_='sense')
        num = 0
        for s in senses:
            if num == 1:
                pass
            definition = s.find('span', class_='def').text
            self.talk(definition)
            time.sleep(1)
            num = 1
        num = 0

    def meaning(self, command):
        words = command.split(' ')
        word = words[-1]
        scrape_url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word
        headers = {"User-Agent": ""}
        web_response = requests.get(scrape_url, headers=headers)

        if web_response.status_code == 200:
            soup = BeautifulSoup(web_response.text, 'html.parser')

            try:
                # show_origin(soup)
                self.show_definitions(soup)
            except AttributeError:
                self.talk('Word not found!!')
        else:
            self.talk('Failed to get response...')

    ###

    # support function that provides a random useless fun fact from a website
    # used an api call to hold data in a list
    # api from: https://uselessfacts.jsph.pl/

    def give_fun_fact(self):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.request("GET", url)
        data = json.loads(response.text)
        fact = data['text']
        return fact

    def fact(self):
        fact = self.give_fun_fact()
        self.talk(fact)

    ###

    #functions to provide a quote randomly from the first page of goodreads.com using web scraping
    #They are: random_quote, scrape_website, quote
    #The code was followed according to this tutorial video: https://www.youtube.com/watch?v=gH0Winlel4Q

    def random_quote(self, quoteList, AuthorList):
        length = len(quoteList)
        num = random.randrange(length - 1)
        return quoteList[num] + " by " + AuthorList[num]

    def scrape_website(self, page_num):
        # list for the author and quotes
        authors = []
        quotes = []

        # Convert the page numbers to a string and add page number to URL, then make a request to the website
        page_num = str(page_num)
        URL = 'https://www.goodreads.com/quotes/tag/inspirational?page=' + page_num
        webpage = requests.get(URL)

        # Parse the text from the website then get the tag and it's class
        soup = BeautifulSoup(webpage.text, "html.parser")
        quoteText = soup.find_all('div', attrs={'class': 'quoteText'})

        for i in quoteText:
            quote = i.text.strip().split('\n')[
                0]  # Get the text of the current quote, but only the sentence before a new line
            author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip()

            quotes.append(quote)
            authors.append(author)

        return authors, quotes

    def quote(self):
        authors, quotes = self.scrape_website(1)
        text = self.random_quote(quotes, authors)
        self.talk(text)

    ###

    # functions that provides a list of statements on a random event that happened on a particular day in history

    def find(self, search_param, occurrence):
        response = requests.get(f'https://en.wikipedia.org/wiki/{search_param}')
        soup = BeautifulSoup(response.text, 'html.parser')
        heading = soup.find(id=occurrence)
        data_list = heading.find_next('ul')
        factList = []
        for data in data_list.find_all('li'):
            factList.append(data.text)
        return factList

    #function for api call to wikipedia to get a list of events that happen on a particular day
    #it uses custom arguments using argparse module that calls an api to scrape data from: https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today
    #code reference: https://github.com/saroz014/this-day-in-history/blob/master/find_this_day.py

    def onThisDay(self):
        MONTHS = {1: ('January', 31),
                  2: ('February', 29),
                  3: ('March', 31),
                  4: ('April', 30),
                  5: ('May', 31),
                  6: ('June', 30),
                  7: ('July', 31),
                  8: ('August', 31),
                  9: ('September', 30),
                  10: ('October', 31),
                  11: ('November', 30),
                  12: ('December', 31)}
        parser = argparse.ArgumentParser(prog='What Happened On This Day',
                                         description='Find out what happened on a particular day in history')
        parser.add_argument('occurrence', nargs='?', default='Holidays_and_observances', type=str,
                            choices=['Events', 'Births', 'Deaths',
                                     'Holidays_and_observances'],
                            help='Name of the occurrence')
        parser.add_argument('-m', '--month', type=int,
                            default=datetime.date.today().month, choices=range(1, 13), help='Month to be looked')
        parser.add_argument('-d', '--day', type=int,
                            default=datetime.date.today().day, help='Day to be looked')
        args = parser.parse_args()

        month_day_tuple = MONTHS[args.month]

        if not 1 <= args.day <= month_day_tuple[1]:
            parser.error(
                f"argument -d/--day: invalid choice: {args.day} (choose from {', '.join(map(repr, range(1, month_day_tuple[1] + 1)))})")
        else:
            search_param = f'{month_day_tuple[0]}_{args.day}'

        dateList = self.find(search_param, args.occurrence)

        temp = random.choice(dateList)

        print("One of the many things things today is known for is " + temp)
        self.talk("One of the many things things today is known for is " + temp)

    def shut(self):
        self.talk("Personal Voice Assistant Shutting Down")
        exit()

    def functions(self):
        self.talk(
            "Asking me to open youtube, wikipedia or google. I can also tell you the time, date or even say jokes. Try me!"
            "")

    def Processo_r(self):
        command = str(self.speech_recog())

        if command == "what can you do":
            self.functions()
            v.set("Asked for help")

        elif 'hello' in command or 'hi' in command:
            self.greet()
            v.set("Greetings")

        elif 'who are you' in command:
            self.introduction()

        elif 'what day' in command:
            self.tell_day()
            v.set("Asked what day")

        elif 'what month' in command:
            self.tell_month()
            v.set("Asked what month")

        elif 'time' in command:
            self.tell_time()
            v.set("Asked what time")

        elif 'google' in command:
            self.openGoogle()
            v.set("Opened google")

        elif 'youtube' in command:
            self.openYoutube()
            v.set("Opened youtube")

        elif 'wikipedia' in command:
            self.openwiki()
            v.set("Opened wikipedia")

        elif 'who is' in command:
            self.openwikiperson(command)
            v.set("Searched for a person")

        elif 'calendar' in command:
            self.openCal()
            v.set("Opened Googgle calendar")

        elif 'mean' in command:
            self.meaning(command)
            v.set("Searched word meaning")

        elif 'where is' in command:
            self.where(command)
            v.set("Searched location")

        elif 'joke' in command:
            self.jokes()
            v.set("Provided a random joke")

        elif 'play' in command:
            self.playMusic(command)
            v.set("Played requested music")

        elif 'fact' in command:
            self.fact()
            v.set("Provided a random fact")

        elif 'quote' in command:
            self.quote()
            v.set("Provided a random quote")

        elif 'on this day' in command:
            self.onThisDay()
            v.set("Informed about today in history")

        elif 'stop' in command or 'exit' in command or 'bye' in command:
            self.shut()

        elif app_string[0] in command:
            os.startfile(app_dest + app_link[0])

            self.talk("Microsoft office Word is opening now")

        elif app_string[1] in command:
            os.startfile(app_dest + app_link[1])
            self.talk("Microsoft office PowerPoint is opening now")

        elif app_string[2] in command:
            os.startfile(app_dest + app_link[2])
            self.talk("Microsoft office Excel is opening now")

        elif app_string[3] in command:
            os.startfile(app_dest + app_link[3])
            self.talk("Zoom is opening now")

        elif app_string[4] in command:
            os.startfile(app_dest + app_link[4])
            self.talk("Notepad is opening now")

        elif app_string[5] in command:
            os.startfile(app_dest + app_link[5])
            self.talk("Google chrome is opening now")

        else:
            self.talk("I don't quite understand what you want me to do")


root = Tk()
app = Window(root)
root.geometry("400x400")
root.iconbitmap("robo.ico")

myImg = ImageTk.PhotoImage(Image.open("robot.jpg"))
imgLabel = Label(root, image=myImg)
imgLabel.grid(row=2, column=1)

v = StringVar()
placeLabel = Label(root, textvariable=v)
placeLabel.grid(row=5, column=0, columnspan=2)

root.mainloop()
