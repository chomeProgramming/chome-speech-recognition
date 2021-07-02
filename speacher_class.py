import sys
import re
import speech_recognition
import os
import pyttsx3

recognizer = speech_recognition.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.runAndWait()

class ChomeSpeacher():
    def __init__(self, appName, listenWord):
        self.appName = appName
        self.listenWord = listenWord
        self.listenWordEnd = "run"
        self.askType = "listen"

    def say(self, output):
        print(output)
        pyttsx3.speak(output)
    def output(self, output):
        print("output: " + output)
        pyttsx3.speak(output)

    def runCommand(self, newCommand):
        # newCommand = newCommand.split(" ")
        # if (newCommand[0].lower() != self.listenWord):
        #     return print("Wrong listener word.")
        # if (len(newCommand) < 2):
        #     return self.output("Parameters are wrong.")

        # newCommand = {
        #     "paramCount": len(newCommand) - 1,
        #     "command": newCommand[1].lower(),
        #     "value": " ".join(newCommand[2:]),
        #     "valueList": newCommand[2:]
        # }

        self.commandHandler(newCommand)

    def commandAsk(self):
        if self.askType == "write":
            self.commandInput()
        elif self.askType == "listen":
            self.commandListener()

    def commandInput(self):
        newCommand = input()
        self.runCommand(newCommand)
        self.commandAsk()

    def commandListener(self):
        answer = ""
        with speech_recognition.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                # audio = recognizer.listen(speech_recognition.Microphone())
                answer = recognizer.recognize_google(
                    audio, key=None, language="en-US", show_all=False
                )
            except speech_recognition.UnknownValueError:
                print("UnknownValueError")
        print(answer)
        self.runCommand(answer)
        answer = None
        self.commandAsk()

    def scanText(self, text):
        result = []
        lv_text = text
        while lv_text.find(self.listenWord) != -1:
            newValue = lv_text[ lv_text.find(self.listenWord): ]

            if newValue.rfind(self.listenWord) != 0:
                newValue = newValue[: newValue[ len(self.listenWord): ].find(self.listenWord) + len(self.listenWord)]

            newValue = newValue.split(" ")
            while (newValue[-1] == "" or newValue[-1] == " "):
                newValue = newValue[:-1]
            newValue = " ".join(newValue)

            if (newValue.split(" ")[-1] == "run"):
                result.append({
                    "full": newValue,
                    "param": newValue.split(" ")[1],
                    "values": " ".join(newValue.split(" ")[2:-1]),
                    "valuesList": newValue.split(" ")[2:-1],
                })

            lv_text = lv_text[len(newValue):]

        return result

    def detectMarks(self, text):
        self.replaceMarks = [ ["dot","."] ]

        text = text.split(" ")
        for mark in self.replaceMarks:
            while mark[0] in text:
                position = text.index(mark[0])
                if position == 0:
                    text[position + 1] = mark[1] + text[position + 1]
                elif position == len(text)-1:
                    text[position - 1] += mark[1]
                else:
                    text[position - 1] += mark[1] + text[position + 1]
                    text.pop(position + 1)
                text.pop(position)                

        return " ".join(text)

    def commandHandler(self, command):
        if (self.askType == "listen"):
            command = self.detectMarks(command.lower())
        founds = self.scanText(command)

        for found in founds:

            if (found["param"] == "open"):
                currentCommand = "start %s" % found["values"]
                if os.system(currentCommand) == 0:
                    self.output(f"starting {found['valuesList'][0]}")
                else:
                    self.output(f"Can\'t open \"%s\"." % (found["values"]))

            elif found["param"] == "exit":
                self.output("exiting")
                sys.exit(1)
            elif found["param"] == "help":
                self.output("writing help")
                print(f'\nYou can start commands in this app with saying \"{self.listenWord}\" at beginning and say the command after that.\
                    \nIf you want to write something because you want to enter a link exactly, you can say: \"{self.listenWord} type enter\".\
                    \nIf you then want to be able to speak again, you say: \"{self.listenWord} type listen\".\
                    \nRead the introduction for more informations.\n\
                ')

            elif found["param"] == "type":
                if found["value"] == "listen":
                    self.askType = "listen"
                    self.output("changing to listen mode")
                elif found["value"] == "enter":
                    self.askType = "write"
                    self.output("changing to write mode")

            else:
                self.output("Command does not exist.")

        if (len(founds) > 0):
            return True
        else:
            return False