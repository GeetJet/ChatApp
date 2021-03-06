import nltk
import pyttsx3
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import speech_recognition as sr
import os
import matplotlib
import fitz
import subprocess
from PyPDF2 import PdfFileReader

matplotlib.use('Agg')
from matplotlib import pyplot


def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    inp = r.recognize_google(audio)
    print(inp)
    return inp


def qna_response(user_request):
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

    def greeting(sentence):
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def spf():
        path_to_pdf = os.path.abspath(out + ".pdf")
        # testing this on my Windows Install machine
        process = subprocess.Popen(path_to_pdf, shell=True)
        process.wait()
        #print(out + '.pdf')
        os.remove(out + '.pdf')

    def speak():
        # # Speaking rate
        voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

        # Use female voice
        engine = pyttsx3.init()
        engine.setProperty('rate', 200)  # setting up new voice rate
        engine.setProperty('voice', voice_id)
        # engine.runAndWait()
        # rate = engine.getProperty('rate')  # getting details of current speaking rate
        print('speaking')
        engine.say(bot_response)
        engine.runAndWait()
        engine.stop()



    #directory = r'C:\Users\Gjeethwani\PycharmProjects\pythonProject\chatbot'
    directory = r'C:\Users\Gjeethwani\PycharmProjects\pythonProject\chatapp'
    bot_response = ''
    instnce = 0
    j = 0
    if (user_request != 'hi'):

        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                doc = fitz.open(filename)
                fpath = os.path.join(directory, filename)
                pdf = PdfFileReader(open(fpath, 'rb'))
                pno = pdf.getNumPages()
                print(filename, pno)
                pno = pno - 1
                for i in range(1):

                    # if(j==0):

                    page = doc[i]
                    # print("Processing page: " + str(i))
                    j = i

                    ### SEARCH

                    text = user_request
                    text_instances = page.searchFor(text)

                    ### HIGHLIGHT
                    # if(text_instances):
                    for inst in text_instances:
                        highlight = page.addHighlightAnnot(inst)
                        out = "output" + str(i + 1)
                        if (instnce == 0):
                            arr1 = i
                        instnce = 1

                if (instnce == 1):
                    doc.save(out + ".pdf", garbage=4, deflate=True, clean=True)
                    spf()
                    #os.startfile(out + ".pdf")
                instnce = 0
            else:
                continue
        bot_response = "searched all files for " + user_request
    elif (greeting(user_request) != None):
        bot_response = greeting(user_request)
    speak()
    return bot_response
