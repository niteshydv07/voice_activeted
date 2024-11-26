import speech_recognition as sr
import pyttsx3
import requests
import datetime
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
# Set properties for speech rate (words per minute)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 10)  # Decrease the rate by 150

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's voice command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            speak("Sorry, my speech service is down.")
            return ""

# Function to set reminders
def set_reminder(time_str, message):
    try:
        reminder_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        speak(f"Reminder set for {reminder_time}")
        while datetime.datetime.now() < reminder_time:
            time.sleep(1)
        speak(f"Reminder: {message}")
    except ValueError:
        speak("The date format is incorrect. Please provide it in 'YYYY-MM-DD HH:MM:SS' format.")

# Function to check the weather
def get_weather(city):
    api_key = '8e41e012ca560fed7ef9d68a90fc39f3'  # Your actual OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        weather_report = f"The temperature in {city} is {temperature}°C with {description}."
        speak(weather_report)
    else:
        speak("City not found.")

# Function to read the news
def get_news():
    api_key = '4f8885d3b2454f25ad3f48006cbedeef'  # Your actual NewsAPI key
    base_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(base_url)
    articles = response.json()["articles"]
    
    for i, article in enumerate(articles[:5], 1):
        speak(f"News {i}: {article['title']}")

# Main function to handle user commands
def main():
    speak("How can I help you today?")
    while True:
        command = listen()
        
        if 'reminder' in command:
            speak("What is the reminder?")
            message = listen()
            if message:
                speak("When should I remind you? Please say in 'YYYY-MM-DD HH:MM:SS' format.")
                time_str = listen()
                if time_str:
                    set_reminder(time_str, message)
        
        elif 'weather' in command:
            speak("Which city and country do you want the weather for?")
            city = listen()
            if city:
                get_weather(city)
        
        elif 'news' in command:
            speak("Here are the top news headlines:")
            get_news()
        
        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break


if __name__ == "__main__":
    main()
