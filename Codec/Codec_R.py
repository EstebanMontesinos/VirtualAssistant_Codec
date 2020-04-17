from gtts import gTTS
import speech_recognition as sr
from pygame import mixer
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import smtplib
import bs4
import requests


def speak(audio): #we are passing audio as an argument to let codec speak.
    print(audio)
    for line in audio.splitlines(): #program will loop lines with the help of splitlines().This method is used to split the lines at line boundaries.
        text_to_speech = gTTS(text=audio, lang="en-us")#GTTS will convert all these text to speech.
        text_to_speech.save('audio.mp3') #Once loop finished, save() method writes result to file.
        mixer.init()#Pygame mixer is a module used foor loading and playing sounds and must be initialized before using it.
        mixer.music.load("audio.mp3")
        mixer.music.play()

def myCommand():
    r = sr.Recognizer()#You need to initialize the recognizer
    print(sr.Microphone.list_microphone_names())  # print all the microphones connected to your machine
    with sr.Microphone()as source:
        print("Codec is ready....")
        r.pause_threshold = 1 #waits for one second to let the recognizer adjust to the sorrounding noise level.
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("You said:" + command + '\n')

    except sr.UnknownValueError:
        print("Your command couldn't be heard")
        command = myCommand() #Uses a recursive call to loop back  if command couldnt be heard or recognized.
    return command

def codec(command):
    errors=[ #Erorrs
        "Sorry i didnt quite get that",
        "Could you please repeat that",
        "Excuse me",
    ]
    #Web automation
    if "hello" in command:
        speak("Hello I am Codec. How can I help you?")
        time.sleep(3)

    elif 'open google and search' in command:
        RegE = re.search('open google and search (.*)', command) #uses regular  expresions import re (.*) will add that to a capture group.
        search_for = command.split("search", 1)[1] #use group 1 to search appropriately.
        url = 'https://www.google.com/'
        if RegE:
            subgoogle = RegE.group(1)
            url = url + 'r/' + subgoogle
        speak('You got it! Opening google now')
        driver = webdriver.Chrome('/Users/estebanmontesinos/Downloads/chromedriver')  # must select specific file.
        driver.get('http://www.google.com')
        search = driver.find_element_by_name('q')  # finds search bar by looking at inspect element
        search.send_keys(str(search_for))  # sends search keys  and converts search for into a string based on command
        search.send_keys(Keys.RETURN)  # hits return key

    #Email command.
    elif 'email' in command:
        speak("Type email target below")
        receiver_email= str(input("Type email target here:"))
        sender_email = "esteban.montesinos.services@gmail.com" #Place your email here
        speak('What is the subject?')
        time.sleep(3)
        subject = myCommand()
        speak('What message should I send?')
        time.sleep(3)
        message = myCommand()
        content = 'Subject: {}\n\n{}'.format(subject, message)
        mail = smtplib.SMTP('smtp.gmail.com', 587) # init gmail SMTP
        mail.ehlo() #identify to server
        mail.starttls() # encrypt session
        mail.login(sender_email, 'Nico201996')#Log ins
        mail.sendmail(sender_email, receiver_email,content)#sends message
        mail.close()
        speak('Email sent.')

    #In order to crawl data we will use beautifulsoup4 a Python library for pulling data out of HTML and XML files.

    elif 'wikipedia' in command:
        RegE = re.search('search in wikipedia (.+)', command)
        if RegE:
            query = command.split()
            response = requests.get("https://en.wikipedia.org/wiki/" + query[3])

            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')#converts html text to normal text
                paragraphs = html.select("p")
                for i in paragraphs:
                    print (i)
                intro = '\n'.join([i.text for i in paragraphs[0:5]])
                print(intro)
                mp3name = 'speech.mp3'
                language = 'en-us'
                myobj = gTTS(text=intro, lang=language, slow=False)
                myobj.save(mp3name)
                mixer.init()
                mixer.music.load("speech.mp3")
                mixer.music.play()
            elif 'stop' in command:
                mixer.music.stop()

    else:
        error = random.choice(errors)
        speak(error)
        time.sleep(3)



#main
speak("Codec is ready!")
time.sleep(3)
while True:
    codec(myCommand())#we pass our command function to listen to  audio
    
    











