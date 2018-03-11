from gtts import gTTS
from os import system
import subprocess
import speech_recognition as sr
import pyttsx

# AIzaSyBIYD_ZwO06008JMay_ieeOqCDesPaExvE 
#youdontmesswithtinson

def listen():
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)
    try:
        print("You said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Could not understand audio")

def say(verses):
    engine = pyttsx.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'english+f3')
    engine.setProperty('rate', 165)
    print "Bot : " + verses
    engine.say(verses)
    engine.runAndWait()

def Inform(verses):
    say(verses)

def say2(verses, file = "speakfile"):
    speech = gTTS(text=verses, lang = 'en', slow = False)
    file = file + ".wav"
    speech.save(file)
    cmd = "mpg321 " + file
    system(cmd)

if __name__ == '__main__':
    #say("The quick brown fox jumped over the lazy cat. Eva Eva Eva")
    say("Eevah is Eevah, so is Eevah")
    #listen() 
