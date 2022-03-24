import pyttsx3
import speech_recognition as sr
import os
import pickle
import random
from colorama import Fore, Style, Back
from django.shortcuts import render
from django.http import HttpResponse
import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import colorama
colorama.init

with open('E:\\Mca6sem\\project\\NUBI\\static\\intents.json') as file:
    data = json.load(file)
r = sr.Recognizer()


def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def index2(request):
    return render(request, 'index.html')


model = keras.models.load_model(
    'E:\\Mca6sem\\project\\NUBI\\static\\chat_model')
with open('E:\\Mca6sem\\project\\NUBI\\static\\tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('E:\\Mca6sem\\project\\NUBI\\static\\lbl_encoder.pickle', 'rb') as ecn:
    lbl_encoder = pickle.load(ecn)
max_len = 20

while(1):

    try:

        with sr.Microphone() as source2:

            r.adjust_for_ambient_noise(source2, duration=0.2)

            audio2 = r.listen(source2)

            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print('User :' + MyText)
            if MyText.lower() == "goodbye":
                break

            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([MyText]),
                                                                              truncating='post', maxlen=max_len))

            tag = lbl_encoder.inverse_transform([np.argmax(result)])
            for i in data['intents']:
                if i['tag'] == tag:
                    print(Fore.GREEN + "NUBI: " + Style.RESET_ALL,
                          np.random.choice(i['responses']))
                    print("Did you say "+np.random.choice(i['responses']))
                    SpeakText(np.random.choice(i['responses']))

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        SpeakText("I'm sorry, but I'm unable to hear you.")
        print(Fore.GREEN + "NUBI: "+"I'm sorry, but I'm unable to hear you.")
