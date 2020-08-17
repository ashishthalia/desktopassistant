import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import json
from youtubesearchpython import SearchVideos
from googlesearch import search
import smtplib
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
r = sr.Recognizer()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good Morning')
    elif hour>=12 and hour<18:
        speak('Good Afternoon')
    else:
        speak('Good evening')
    speak('I am Tokyo!. Please tell me How may I help you!')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=8)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') 
        print(f"User said: {query}\n")  

    except Exception as e:
        
        print("Say that again please...")   
        return "None" 
    return query
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('niceash99@gmail.com', 'helenkeler')
    server.sendmail('niceash99@gmail.com',to, content)
    server.close()
    

if __name__ == "__main__":
    wish()
    while True:
    
        query = takeCommand().lower() 
        if 'wikipedia' in query:  
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            print(query)
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        elif "open stackoverflow" in query:
            webbrowser.open("stackoverflow.com")
        elif "play" and "in youtube" in query:
            speak("Please Wait")
            query = query.replace("in youtube","")
            print(query)
            search1 = SearchVideos(query, offset=1, mode="json", max_results=5)
            results = search1.result()
            results = json.loads(results)
            link=results["search_result"][0]["link"]
            webbrowser.open(link)
        elif "open google" in query:
            webbrowser.open("google.com")
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
        elif "mail" in query:
            try:
                speak("Please tell me the receipent")
                to = takeCommand()
                speak("What should I write in mail?")
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry I am not able to send this mail please check security issues")
        elif 'search' and 'on google' in query:
            query = query.replace('on google','')
            query = query.replace('search','')
            print("Searching")
            speak("Here are some links I found for you")
            for j in search(query, tld="co.in", num = 10, stop=10, pause=2):
                print(j)