from subprocess import run
import sys
import re
# import webbrowser
import speech_recognition
import os

import pyttsx3

# speaking + apps: https://www.geeksforgeeks.org/open-applications-using-python/

recognizer = speech_recognition.Recognizer()

listenWord = "alexa"

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.runAndWait()

# webbrowser.register("chrome",
#     None,
#     webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe")
# )

def runCommand(newCommand):
    engine.say('Hello World!!')
    pyttsx3.speak("Welcome to my tools")

    newCommand = newCommand.split(" ")
    if (newCommand[0].lower() != listenWord or len(newCommand) < 3):
        return print("Command is written wrong.")
    newCommand = {
        "command": newCommand[1].lower(),
        "value": " ".join(newCommand[2:len(newCommand)])
    }

    if (newCommand["command"] == "open"):
        try:
            # webbrowser.get("chrome").open(newCommand["value"])
            currentCommand = f"start {newCommand['value']}"
            print(currentCommand)
            os.startfile(currentCommand + ".exe")
            # os.system(currentCommand)
        except:
            print(f"Error happend at: opening \"%s\"" % (newCommand["value"]))
    else:
        print("Command does not exist or you wrote it wrong.")

def commandInput():
    newCommand = input()
    runCommand(newCommand)
    commandInput()

def commandListener():
    answer = ""
    with speech_recognition.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        answer = recognizer.recognize_google(
            audio, key=None, language="en-US", show_all=False
        )
    except speech_recognition.UnknownValueError:
        print("UnknownValueError")
    print(answer)
    runCommand(answer)
    answer = None
    commandListener()

# commandListener()
commandInput()