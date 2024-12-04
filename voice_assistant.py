import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        command = ""
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, I'm unable to connect to the service.")
        return command.lower()

def respond(command):
    if "hello" in command:
        speak("Hello, how can I assist you today?")
    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time}")
    elif "date" in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {date}")
    elif "search" in command:
        speak("What would you like to search for?")
        search_query = listen_command()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Here are the results for {search_query}")
    elif "bye" in command:
        speak("Goodbye, have a nice day!")
        exit()

if __name__ == "__main__":
    speak("Hello, I am your voice assistant. How can I help you today?")
    
    while True:
        command = listen_command()
        respond(command)
