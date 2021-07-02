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
listenWord = "alexa"

speacher = ChomeSpeacher(appName, listenWord)
def startSpeacher():
    os.system("cls")
    speacher.say("Welcome to %s!\n" % appName)
    # speacher.askType = "write"
    # speacher.commandInput()
    speacher.commandListener()

startSpeacher()

# next step:
    # vosk speech_recognition:
    # https://www.youtube.com/watch?v=Itic1lFc4Gg

# vosk: https://www.youtube.com/watch?v=xAdqA1prU5s