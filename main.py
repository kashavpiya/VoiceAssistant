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
#import pyowm
import webbrowser
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

class Window(Frame):
    def __init__(self, master):
        self.master = master
        master.title("Summer")

        A = Label(master, text="Hi! I am Summer, your voice assistant")
        A.grid(row=0, column = 1, columnspan=2)

        clicked = StringVar()
        clicked.set("Functions:")
        dropList = ["Tell time","Tell Date", "Play Music", "Introduction", "Search Person", "Play Youtube", "Search wiki", "This day info", "Say Fact, Quote, or Joke", "Locate", "Find meaning", "Functions:"]
        drop = OptionMenu(master, clicked, *dropList)
        drop.grid(row = 0, column = 0)

        # myImg = ImageTk.PhotoImage(Image.open("robot.jpg"))
        # imgLabel = Label(master, image = myImg)
        # imgLabel.grid(row=2, column = 1)

        listenButton = Button(master, text = "Listen!", width = 25, command = self.Processo_r, fg="yellow", bg="#000000")
        listenButton.grid(row = 3, column = 1)

        button_quit = Button(master, text= "Exit", command=root.quit)
        button_quit.grid(row = 3, column = 2)
        
        myLabel2 = Label(master, text = "Logs:")
        myLabel2.grid(row = 4, column = 0)
              

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
        messages = ["Hi,nice to meet you","hello","Nice to meet you","hey,nice to meet you","good to meet you!"]
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
                show_definitions(soup)
            except AttributeError:
                self.talk('Word not found!!')
        else:
            self.talk('Failed to get response...')

    def fact(self):
        fact = give_fun_fact()
        self.talk(fact)

    def quote(self):
        authors, quotes = scrape_website(1)
        text = random_quote(quotes, authors)
        self.talk(text)

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
        dateList = find(search_param, args.occurrence)

        temp = random.choice(dateList)
        print("One of the many things things today is known for is " + temp)
        self.talk("One of the many things things today is known for is " + temp)

    def shut(self):
        self.talk("Personal Voice Assistant Shutting Down")
        exit()

    def functions(self):
        self.talk("Asking me to open youtube, wikipedia or google. I can also tell you the time, date or even say jokes. Try me!"
             "")
    def Processo_r(self):
        command = str(self.speech_recog())

        if command == "What can you do":
            self.functions()

        elif 'who are you' in command:
            self.introduction()

        elif 'what day' in command:
            self.tell_day()

        elif 'what month' in command:
            self.tell_month()

        elif 'time' in command:
            self.tell_time()

        elif 'google' in command:
            self.openGoogle()

        elif 'youtube' in command:
            self.openYoutube()

        elif 'wikipedia' in command:
            self.openwiki()

        elif 'who is' in command:
            self.openwikiperson(command)

        elif 'calendar' in command:
            self.openCal()

        elif 'mean' in command:
            self.meaning(command)

        elif 'where is' in command:
            self.where(command)

        elif 'joke' in command:
            self.jokes()

        elif 'play' in command:
            self.playMusic(command)

        elif 'fact' in command:
            self.fact()

        elif 'quote' in command:
            self.quote()

        elif 'on this day' in command:
            self.onThisDay()

        elif 'stop' in command or 'exit' in command or 'bye' in command:
            self.shut()

        else:
            self.talk("I don't quite understand what you want me to do")



root=Tk()
app=Window(root)
root.geometry("400x400")
root.iconbitmap("robo.ico")

myImg = ImageTk.PhotoImage(Image.open("robot.jpg"))
imgLabel = Label(root, image = myImg)
imgLabel.grid(row=2, column = 1)
root.mainloop()


def scrape_website(page_number):
    # list for the author and quotes
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
        quote = i.text.strip().split('\n')[
            0]  # Get the text of the current quote, but only the sentence before a new line
        author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip()

        quotes.append(quote)
        authors.append(author)

    return authors, quotes


# support function to give a random quote from list
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


def find(search_param, occurrence):
    response = requests.get(f'https://en.wikipedia.org/wiki/{search_param}')
    soup = BeautifulSoup(response.text, 'html.parser')
    heading = soup.find(id=occurrence)
    data_list = heading.find_next('ul')
    factList = []
    for data in data_list.find_all('li'):
        factList.append(data.text)
    return factList

#
# """
# this function is used to take command from the user
# whenever the function is called, it will start listening, convert speech to text,
# replaces the wakeword with a blank space
# if the wake word is detected in the command, the string with the command is return,
# else none is returned
# """
#
#
# def take_command():
#     try:
#         with sr.Microphone() as source:
#             dummy.set("Listening...")
#             print("Listening...")
#             voice = listener.listen(source)
#             command = listener.recognize_google(voice)
#             command = command.lower()
#             if 'summer' in command:
#                 command = command.replace('summer', '')
#                 dummy.set(command)
#                 print(command)
#             else:
#                 dummy.set("Pardon me, please say that again")
#                 talk("Pardon me, please say that again")
#                 return "None"
#
#     except Exception as e:
#         talk("Pardon me, please say that again")
#         return "None"
#
#     return command
#
#
# """
# this function is the conditional function of the virtual assistant where all the conditions
# for each command is provided.
# """
#
#
# def run_summer(command):
#     print(command)
#
#     # plays any song or video on youtube
#     if 'play' in command:
#         song = command.replace('play', '')
#         talk('playing' + song)
#         pywhatkit.playonyt(song)
#
#     # ask summer about itself
#     elif 'who are you' in command:
#         talk("I am Summer, your personal voice assistant or something like that, I don't really know yet.")
#
#     # ask about time
#     elif 'time' in command:
#         timer = datetime.datetime.now().strftime('%I:%M %p')
#         print(timer)
#         talk("The current time is" + timer)
#
#     # ask who a person or a name is
#     elif 'who is' in command:
#         person = command.replace('who is', '')
#         info = wikipedia.summary(person, 1)
#         talk("According to Wikipedia,")
#         print(info)
#         talk(info)
#
#     # open wikipedia
#     elif 'open wikipedia' in command:
#         webbrowser.open_new_tab("https://en.wikipedia.org/wiki/Main_Page")
#         talk("Opening Wikipedia")
#         time.sleep(5)
#
#     # open wikipedia to search any info
#     elif 'wikipedia' in command:
#         talk('Searching wikipedia...')
#         command = command.replace("wikipedia", "")
#         info = wikipedia.summary(command, sentences=2)
#         talk("According to Wikipedia,")
#         print(info)
#         talk(info)
#
#     # summer tells you a joke
#     elif 'joke' in command:
#         joke = pyjokes.get_joke()
#         print(joke)
#         talk(joke)
#
#     # opens youtube
#     elif 'open youtube' in command:
#         webbrowser.open_new_tab("https://www.youtube.com")
#         talk("Opening YouTube")
#         time.sleep(5)
#
#     # opens your gmail if logged in
#     elif 'open gmail' in command:
#         webbrowser.open_new_tab("https://www.gmail.com")
#         talk("Opening Gmail")
#         time.sleep(5)
#
#     # opens google search page
#     elif 'open google' in command:
#         webbrowser.open_new_tab("https://www.google.com")
#         talk("Opening Google")
#         time.sleep(5)
#
#     # opens google calendar if logged in
#     elif 'open calendar' in command:
#         webbrowser.open_new_tab("https://calendar.google.com")
#         talk("Opening your calendar")
#         time.sleep(5)
#
#     # tells you where a place is
#     elif 'where is' in command:
#         words = command.split('where is')
#         print(words[-1])
#         link = str(words[-1])
#         link = re.sub(' ', '', link)
#         talk('Locating')
#         time.sleep(2)
#         talk(link)
#         time.sleep(4)
#         link = f'https://www.google.co.in/maps/place/{link}'
#         print(link)
#         webbrowser.open(link)
#
#     # tells you the meaning of a word
#     elif 'meaning' in command:
#         print('..')
#         words = command.split(' ')
#         word = words[-1]
#         scrape_url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word
#         print(words[-1])
#         headers = {"User-Agent": ""}
#         web_response = requests.get(scrape_url, headers=headers)
#
#         if web_response.status_code == 200:
#             soup = BeautifulSoup(web_response.text, 'html.parser')
#
#             try:
#                 # show_origin(soup)
#                 show_definitions(soup)
#             except AttributeError:
#                 talk('Word not found!!')
#         else:
#             talk('Failed to get response...')
#
#     # tells you what the weather is in your location
#     elif 'weather' in command:
#         print('..')
#         words = command.split('in')
#         print(words[-1])
#         scrape_weather(words[-1])
#
#
#     # tells you the fact of the day
#     elif 'fact' in command:
#         fact = give_fun_fact()
#         print(fact)
#         talk(fact)
#
#     # gives you a quote
#     elif 'quote' in command:
#         authors, quotes = scrape_website(1)
#         text = random_quote(quotes, authors)
#         print(text)
#         talk(text)
#
#     # this day in history
#     elif 'today' in command or 'this day' in command:
#         MONTHS = {1: ('January', 31),
#                   2: ('February', 29),
#                   3: ('March', 31),
#                   4: ('April', 30),
#                   5: ('May', 31),
#                   6: ('June', 30),
#                   7: ('July', 31),
#                   8: ('August', 31),
#                   9: ('September', 30),
#                   10: ('October', 31),
#                   11: ('November', 30),
#                   12: ('December', 31)}
#         parser = argparse.ArgumentParser(prog='What Happened On This Day',
#                                          description='Find out what happened on a particular day in history')
#         parser.add_argument('occurrence', nargs='?', default='Holidays_and_observances', type=str,
#                             choices=['Events', 'Births', 'Deaths',
#                                      'Holidays_and_observances'],
#                             help='Name of the occurrence')
#         parser.add_argument('-m', '--month', type=int,
#                             default=datetime.date.today().month, choices=range(1, 13), help='Month to be looked')
#         parser.add_argument('-d', '--day', type=int,
#                             default=datetime.date.today().day, help='Day to be looked')
#         args = parser.parse_args()
#         month_day_tuple = MONTHS[args.month]
#         if not 1 <= args.day <= month_day_tuple[1]:
#             parser.error(
#                 f"argument -d/--day: invalid choice: {args.day} (choose from {', '.join(map(repr, range(1, month_day_tuple[1] + 1)))})")
#         else:
#             search_param = f'{month_day_tuple[0]}_{args.day}'
#         dateList = find(search_param, args.occurrence)
#
#         temp = random.choice(dateList)
#         print("One of the many things things today is known for is " + temp)
#         talk("One of the many things things today is known for is " + temp)
#
#     # tells summer to stop talking, summer shuts down
#     elif 'stop' in command or 'exit' in command or 'bye' in command:
#         return
#
# """
#     elif 'change code' or 'change lock' in command:
#         file.write("true")
#         talk("please give a code")
#         order = take_command().lower()
#         codeList = order.split()
#         if checkCode(codeList):
#             file.write(order)
#         else:
#             while checkCode(codeList) is False:
#                 talk("invalid code, please state code again")
#                 order = take_command().lower()
#                 codeList = order.split()
#             file.write(order)
#         print(order)
# """
#
# """
# Supporting function for the conditions above
# """
#
#
# # support function for quote to parse quotes from goodreads.com
# def scrape_website(page_number):
#     # list for the author and quotes
#     authors = []
#     quotes = []
#
#     # Convert the page numbers to a string and add page number to URL, then make a request to the website
#     page_num = str(page_number)
#     URL = 'https://www.goodreads.com/quotes/tag/inspirational?page=' + page_num
#     webpage = requests.get(URL)
#
#     # Parse the text from the website then get the tag and it's class
#     soup = BeautifulSoup(webpage.text, "html.parser")
#     quoteText = soup.find_all('div', attrs={'class': 'quoteText'})
#
#     for i in quoteText:
#         quote = i.text.strip().split('\n')[
#             0]  # Get the text of the current quote, but only the sentence before a new line
#         author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip()
#
#         quotes.append(quote)
#         authors.append(author)
#
#     return authors, quotes
#
#
# # support function to give a random quote from list
# def show_definitions(soup):
#     print()
#     senseList = []
#     senses = soup.find_all('li', class_='sense')
#     num = 0
#     for s in senses:
#         if num == 1:
#             pass
#         definition = s.find('span', class_='def').text
#         talk(definition)
#         time.sleep(5)
#         num = 1
#     num = 0
#
# def random_quote(quoteList, AuthorList):
#     length = len(quoteList)
#     num = random.randrange(length - 1)
#     return quoteList[num] + " by " + AuthorList[num]
#
#
# # support function that provides a random useless fun fact
# def give_fun_fact():
#     url = "https://uselessfacts.jsph.pl/random.json?language=en"
#     response = requests.request("GET", url)
#     data = json.loads(response.text)
#     fact = data['text']
#     return fact
#
#
# # supports the condition that returns the weather
# def scrape_weather(city):
#     url = 'https://www.google.com/search?q=accuweather+' + city
#     page = requests.get(url)
#
#     soup = BeautifulSoup(page.text, 'lxml')
#     links = [a['href'] for a in soup.findAll('a')]
#     link = str(links[16])
#     link = link.split('=')
#     link = str(link[1]).split('&')
#     link = link[0]
#
#     page = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
#     soup = BeautifulSoup(page.content, 'lxml')
#
#     time = soup.find('p', attrs={'class': 'cur-con-weather-card__subtitle'})
#     time = re.sub('\n', '', time.text)
#     time = re.sub('\t', '', time)
#     time = 'Time: ' + time
#     temperature = soup.find('div', attrs={'class': 'temp'})
#     temperature = 'Temperature: ' + temperature.text
#
#     realfeel = soup.find('div', attrs={'class': 'real-feel'})
#     realfeel = re.sub('\n', '', realfeel.text)
#     realfeel = re.sub('\t', '', realfeel)
#     realfeel = 'RealFeel: ' + realfeel[-3:] + 'C'
#     climate = soup.find('span', attrs={'class': 'phrase'})
#     climate = "Climate: " + climate.text
#
#     info = 'For more information visit: ' + link
#
#     print('The weather for today is: ')
#     print(time)
#     print(temperature)
#     print(realfeel)
#     print(climate)
#     print(info)
#     talk('The weather for today is: ')
#     talk(time)
#     talk(temperature)
#     talk(realfeel)
#     talk(climate)
#     talk('For more information visit accuweather.com')
#     time.sleep(5)
#
# # support function for this day in history
#
# def find(search_param, occurrence):
#     response = requests.get(f'https://en.wikipedia.org/wiki/{search_param}')
#     soup = BeautifulSoup(response.text, 'html.parser')
#     heading = soup.find(id=occurrence)
#     data_list = heading.find_next('ul')
#     factList = []
#     for data in data_list.find_all('li'):
#         factList.append(data.text)
#     return factList
#
# # support function to change pass code
# """
# def checkCode(codeList):
#
#     check = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
#     for word in codeList:
#         if word not in check:
#             return False
#     return True
# """
# """
# this is the main function where the entire program starts
# """
# if __name__ == '__main__':
#     talk("Greetings, I am your personal voice assistant.")
#     while True:
#         talk("Tell me how can I help you?")
#         statement = take_command().lower()
#         if statement == 0:
#             continue
#         elif 'stop' in statement or 'bye' in statement or 'exit' in statement:
#             talk("Personal Voice Assistant Shutting Down")
#             exit()
#         else:
#             run_summer(statement)
#         time.sleep(2)
