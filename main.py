import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary
import requests
from google import genai
from gtts import gTTS
import pygame
from dotenv import load_dotenv
import os
import json
from datetime import datetime
recognizer = sr.Recognizer()
newsapi = os.getenv("NEWS_API")
def morningBriefing():

    current_time = datetime.now().strftime("%I:%M %p")

    speak(f"Good morning Shubh")

    speak(f"The time is {current_time}")

    # REMINDERS
    with open("reminders.json", "r") as file:

        reminders = json.load(file)

    if len(reminders) > 0:

        speak(f"You have {len(reminders)} reminders")

        for reminder in reminders:

            speak(reminder)

    else:

        speak("You have no reminders")


    api_key = os.getenv("WEATHER_API")

    city = "New Delhi"

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    response = requests.get(url)

    data = response.json()

    temperature = data["current"]["temp_c"]

    description = data["current"]["condition"]["text"]

    speak(
    f"The temperature in {city} is {temperature} degree Celsius with {description}"
    )
    
def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text,lang='en')
    tts.save('temp.mp3')

    pygame.mixer.init()

    pygame.mixer.music.load("temp.mp3")

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    pygame.mixer.quit()
    time.sleep(1)
    os.remove("temp.mp3")
def aiProcess(command):
    client = genai.Client(api_key=os.getenv("GEMINI_API"))
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"You are Jarvis. Give short concise voice-assistant style responses in under 50 words. {command}"     
)
    text = response.text

    # Remove markdown symbols
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")

    return text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open chrome" in c.lower():
        os.startfile("C:\Program Files\Google\Chrome\Application")

    elif "what do you remember" in c.lower():

        with open("notes.txt", "r") as file:

            notes = file.read()

        print(notes)

        speak(notes)

    elif "remember" in c.lower():

        note = c.replace("remember", "")

        with open("notes.txt", "a") as file:

            file.write(note + "\n")

        speak("I will remember that")

    

    elif "add task" in c.lower():

        task = c.replace("add task", "")

        with open("tasks.txt", "a") as file:

            file.write(task + "\n")

        speak("Task added")

    elif "show task" in c.lower():

        with open("tasks.txt", "r") as file:

            tasks = file.read()

        print(tasks)

        speak(tasks)

    elif "remind me to" in c.lower():

        reminder = c.lower().replace("remind me to", "").strip()

        with open("reminders.json", "r") as file:

            reminders = json.load(file)

        reminders.append(reminder)

        with open("reminders.json", "w") as file:

            json.dump(reminders, file)

        speak("Reminder added")

    elif "tell me my reminders" in c.lower():

        with open("reminders.json", "r") as file:

            reminders = json.load(file)

        if len(reminders) == 0:

            speak("You have no reminders")

        else:

            speak("Here are your reminders")

            for reminder in reminders:

                print(reminder)

                speak(reminder)

    elif "show schedule" in c.lower():
        with open("schedule.json","r") as file:
            schedules = json.load(file)
        if len(schedules) == 0:
            speak("No schedules found")
        else:
            for item in schedules:
                task = item["task"]
                time_ = item["time"]
                print(task, time_)
                speak(f"{task} at {time_}")

    elif "schedule" in c.lower():

        speak("What is the task?")

        with sr.Microphone() as source:

            audio = recognizer.listen(source)

        task = recognizer.recognize_google(audio)

        print("Task:", task)

        speak("At what time? Say in HH MM AM or PM format")

        with sr.Microphone() as source:

            audio = recognizer.listen(source)

        time_input = recognizer.recognize_google(audio)

        print("Time:", time_input)

        with open("schedule.json", "r") as file:

            schedules = json.load(file)

        schedules.append({
            "task": task,
            "time": time_input.upper()
        })

        with open("schedule.json", "w") as file:

            json.dump(schedules, file, indent=4)

        speak("Schedule added")

    elif "good morning" in c.lower():

        morningBriefing()
 

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles[:3]:
                speak(article['title'])
    else:
        # Let GenAI handle the request
        output = aiProcess(c)
        speak(output)
        pass

if __name__ == "__main__":
    speak("Initializing Jarvis.......")
    while True:
        # Listen for the wake word!
        # Obtain Audio from the microphone 
        r = sr.Recognizer()

        print("Recogonizing !")
        try:
            with sr.Microphone() as source : 
                print("Listening !!!!!")
                
                audio = r.listen(source,timeout=5,phrase_time_limit=3)
            word = r.recognize_google(audio)
            print("You said:", word)
            if "jarvis" in word.lower():
                speak("Yeah")
            
                time.sleep(1)
                # Listen for Command
                with sr.Microphone() as source : 
                    print("Jarvis Activated...")
                    
                    audio = r.listen(source)
                command = r.recognize_google(audio) 
                print("Command:", command)

                processCommand(command)
        except Exception as e:
            print("Google Error ; {0}".format(e))

load_dotenv()