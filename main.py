import objc
from Foundation import NSDate, NSRunLoop
from Cocoa import NSSpeechSynthesizer
import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer=sr.Recognizer()
newsapi='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def speak(text):
    tts=gTTS(text)
    tts.save("output.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("output.mp3")
   
def speak_old(text):
    synth = NSSpeechSynthesizer.alloc().initWithVoice_(None)
    synth.startSpeakingString_(text)
    # Run a run loop until speech finishes
    while synth.isSpeaking():
        NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

def aiProcess(command):
    client = OpenAI(
      api_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    )
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general task like alexa and google cloud. Give short responses please."},
        {"role": "user", "content": command}
      ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    if('open google' in c.lower()):
        webbrowser.open("https://google.com")
    elif('open facebook' in c.lower()):
        webbrowser.open("https://facebook.com")
    elif('open instagram' in c.lower()):
        webbrowser.open("https://instagram.com")
    elif('open linkedin' in c.lower()):
        webbrowser.open("https://www.linkedin.com")
    elif('open youtube' in c.lower()):
        webbrowser.open("https://youtube.com")
    elif('open gpt' in c.lower()):
        webbrowser.open("https://chatgpt.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif('news' in c.lower()):
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])
            for article in articles:
                speak(article['title'])
    else:
        # let openAI handle the request
        output = aiProcess(c)
        speak(output)
        

if __name__ == "__main__":
    speak("Initialising Jarvis ...." )
    while True:
        # Listen for the wake word 'Jarvis'
        r=sr.Recognizer()
        #recognise speech using Google
        print("Recognising ...")
        try:
            with sr.Microphone() as source:
                print('Listening ....')
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=='jarvis'):
                speak("Yes Khwaish")
                # listen for command
                with sr.Microphone() as source:
                    print('Jarvis active ....')
                    audio = r.listen(source, timeout=2, phrase_time_limit=1)
                    command = r.recognize_google(audio)
                    processCommand(command)
                    
        except Exception as e:
            print(f"Error : {e}")
