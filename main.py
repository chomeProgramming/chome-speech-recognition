import sys
import re
import speech_recognition
import os
import pyttsx3

from speacher_class import ChomeSpeacher

# speaking + apps: https://www.geeksforgeeks.org/open-applications-using-python/

# pyttsx3.speak("Wilkommen zu meinen Tools") -- can speak German if engine is not set
# engine.say('Hello World!!')

appName = "CHOME SPEACHER"
listenWord = "chome"

speacher = ChomeSpeacher(appName, listenWord)
def startSpeacher():
    # commandListener()
    os.system("cls")
    speacher.say("Welcome to %s!\n" % appName)
    speacher.commandInput()

startSpeacher()