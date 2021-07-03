import sys
import re
import speech_recognition
import os
import pyttsx3
import argparse
import queue
import sounddevice as sd
import vosk

import json

recognizer = speech_recognition.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.runAndWait()

class ChomeSpeacher():
    def __init__(self, appName, listenWord, listenerType, startFunction = None):
        self.appName = appName
        self.listenWord = listenWord
        self.listenWordEnd = "run"
        self.askType = "listen"
        self.listenerType = listenerType
        self.setupData = {}
        self.start = startFunction
        self.setup()

    def say(self, output):
        print(output)
        pyttsx3.speak(output)
    def output(self, output):
        print("output: " + output)
        pyttsx3.speak(output)

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.setupData["q"].put(bytes(indata))

    def start(self):
        return
    def setup(self):
        self.setupData["q"] = queue.Queue()

        def int_or_str(text):
            """Helper function for argument parsing."""
            try:
                return int(text)
            except ValueError:
                return text

        self.setupData["parser"] = argparse.ArgumentParser(add_help=False)
        self.setupData["parser"].add_argument(
            '-l', '--list-devices', action='store_true',
            help='show list of audio devices and exit')
        self.setupData["args"], remaining = self.setupData["parser"].parse_known_args()
        if self.setupData["args"].list_devices:
            print(sd.query_devices())
            self.setupData["parser"].exit(0)
        self.setupData["parser"] = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[self.setupData["parser"]])
        self.setupData["parser"].add_argument(
            '-f', '--filename', type=str, metavar='FILENAME',
            help='audio file to store recording to')
        self.setupData["parser"].add_argument(
            '-m', '--model', type=str, metavar='MODEL_PATH',
            help='Path to the model')
        self.setupData["parser"].add_argument(
            '-d', '--device', type=int_or_str,
            help='input device (numeric ID or substring)')
        self.setupData["parser"].add_argument(
            '-r', '--samplerate', type=int, help='sampling rate')
        self.setupData["args"] = self.setupData["parser"].parse_args(remaining)

        if self.setupData["args"].model is None:
            self.setupData["args"].model = "model"
            if not os.path.exists(self.setupData["args"].model):
                print ("Please download a model for your language from https://alphacephei.com/vosk/models")
                print ("and unpack as 'model' in the current folder.")
                self.setupData["parser"].exit(0)
            if self.setupData["args"].samplerate is None:
                device_info = sd.query_devices(self.setupData["args"].device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                self.setupData["args"].samplerate = int(device_info['default_samplerate'])

            self.setupData["model"] = vosk.Model(self.setupData["args"].model)

            if self.setupData["args"].filename:
                self.setupData["dump_fn"] = open(self.setupData["args"].filename, "wb")
            else:
                self.setupData["dump_fn"] = None

        if (self.start):
            self.start()

    def commandAsk(self):
        if self.askType == "write":
            self.commandInput()
            return "write"
        elif self.askType == "listen":
            if self.listenerType == "vosk":
                self.voskListener()
            else:
                self.commandListener()
            return "listen"

    def commandInput(self):
        newCommand = input()
        self.commandHandler(newCommand)
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
        self.commandHandler(answer)
        answer = None
        self.commandAsk()

    def voskListener(self):
        try:
            with sd.RawInputStream(samplerate=self.setupData["args"].samplerate, blocksize = 8000, device=self.setupData["args"].device, dtype='int16',
                            channels=1, callback=self.callback):
                # print('#' * 80)
                # print('Press Ctrl+C to stop the recording')
                # print('#' * 80)
                rec = vosk.KaldiRecognizer(self.setupData["model"], self.setupData["args"].samplerate)
                while True:
                    if self.askType != "listen":
                        return print("stop")
                    data = self.setupData["q"].get()
                    answer = None
                    if rec.AcceptWaveform(data):
                        resultAudio = json.loads(rec.Result())["text"]
                        if (resultAudio != ""):
                            answer = self.commandHandler(resultAudio)
                    else:
                        resultAudio = json.loads(rec.PartialResult())["partial"]
                        if (resultAudio != ""):
                            answer = self.commandHandler(resultAudio)

                    if (answer == True):
                        rec = vosk.KaldiRecognizer(self.setupData["model"], self.setupData["args"].samplerate)

                    if self.setupData["dump_fn"] is not None:
                        self.setupData["dump_fn"].write(data)

        except KeyboardInterrupt:
            print('\nDone')
            self.setupData["parser"].exit(0)
        except Exception as e:
            self.setupData["parser"].exit(type(e).__name__ + ': ' + str(e))

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
            print(found["full"])

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
                if found["valuesList"][0] == "listen":
                    self.output("changing to listen mode")
                    if self.askType != "listen":
                        self.askType = "listen"
                        self.commandAsk()
                elif found["valuesList"][0] == "enter":
                    self.output("changing to write mode")
                    if self.askType != "write":
                        self.askType = "write"
                        self.commandAsk()

            else:
                self.output("Command does not exist.")

        if (len(founds) > 0):
            return True
        else:
            return False
