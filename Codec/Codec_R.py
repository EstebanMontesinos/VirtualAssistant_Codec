from gtts import gTTS
import speech_recognition as sr
from pygame import mixer

def talk(audio): #we are passing audio as an argument to let codec speak.
    print(audio)
    for line in audio.splitlines(): #program will loop lines with the help of splitlines().This method is used to split the lines at line boundaries.
        TextToSpeech = gTTS(text=audio, lang="en-us")#GTTS will convert all these text to speech.
        TextToSpeech.save('audio.mp3') #Once loop finished, save() method writes result to file.
        mixer.init()#Pygame mixer is a module used foor loading and playing sounds and must be initialized before using it.
        mixer.music.load("audio.mp3")
        mixer.music.play()






