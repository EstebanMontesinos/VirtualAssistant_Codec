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
import urllib.request #used to make requests
import urllib.parse #used to parse values into the url
import webbrowser

def speak(audio): #we are passing audio as an argument to let codec speak.
    print(audio)
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
        mail.login(sender_email, '')#Log ins
        mail.sendmail(sender_email, receiver_email,content)#sends message
        mail.close()
        speak('Email sent.')

    #In order to crawl data we will use beautifulsoup4 a Python library for pulling data out of HTML and XML files.

    elif 'wikipedia' in command:
        RegE = re.search('search in wikipedia (.+)', command)#uses regular  expresions import re (.+) will add that to a capture group.
        if RegE:
            query = command.split()
            response = requests.get("https://en.wikipedia.org/wiki/" + query[3])#URL will look like https://en.wikipedia.org/wiki/Keyword so we are sending get request with keyword

            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')#parses html text to normal text
                paragraphs = html.select("p")#looks for paragraph tag.
                for i in paragraphs:
                    print (i)
                intro = '\n'.join([i.text for i in paragraphs[0:5]])
                print(intro)
                mp3name = 'speech.mp3'
                language = 'en-us'
                text_to_speech = gTTS(text=intro, lang=language, slow=False)
                text_to_speech.save(mp3name)
                mixer.init()
                mixer.music.load("speech.mp3")
                mixer.music.play()
                x = str(input("Press enter to talk to Codec"))

    elif 'youtube' in command:
        speak('Opening youtube now !')
        RegE = re.search('youtube (.+)', command)
        if RegE:
            domain = command.split("youtube", 1)[1]
            query_string = urllib.parse.urlencode({"search_query": domain})#Search key must be encoded before parsing into url.
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})',html_content.read().decode())  # Each video on youtube has its own 11 characters ID the decode() function is used to convert from one encoding scheme, in which argument string is encoded to the desired encoding scheme
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            pass


    elif 'stop' in command:
        mixer.music.stop()

    else:
        error = random.choice(errors)
        speak(error)
        time.sleep(3)



#main
speak("Codec is ready!")
time.sleep(4)
while True:
    codec(myCommand())#we pass our command function to listen to  audio
    
    











