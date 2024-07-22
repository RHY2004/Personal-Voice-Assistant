import pyttsx3
import datetime
import webbrowser
import speech_recognition as sr
import wikipedia
import subprocess
import os
import requests
from google.cloud import aiplatform 


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)

NEWS_API_KEY = 'YOUR API KEY'
GEMINI_API_KEY = 'YOUR API KEY'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening!")
        
    speak("I am Your Personal Voice Assistens. Pleas tell me how may i help you")
    
def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listing....")
        r.pause_threshold = 1
        audio = r.listen(source)
       
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:",query)
        
    except Exception as e:
        print("Say that again please....")
        return "None"
    return query



#Logic to open Application on device 
def open_application(app_name):
    if 'notepad' in app_name:
        subprocess.Popen(['notepad.exe'])
    elif 'calculator' in app_name:
        subprocess.Popen(['calc.exe'])
    elif 'chrome' in app_name:
        subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])  # Path to Chrome
    # Add more applications as needed
    else:
        speak("Application not found")
        

#Logic to play music
def play_music():
    music_dir = 'D:\\Music'  
    if os.path.exists(music_dir):
        music_files = os.listdir(music_dir)
        if music_files:
            speak("Playing music")
            os.startfile(os.path.join(music_dir, music_files[0]))  # Play the first music file in the directory
        else:
            speak("No music files found in the directory")
    else:
        speak("Music directory not found")    
        
        
#Logic to Read News
def get_news():
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news_data = response.json()
    
    articles = news_data.get('articles')
    if articles:
        speak("Here are the top news headlines")
        for i, article in enumerate(articles[:5]):  # Read top 5 headlines
            headline = article['title']
            speak(f"Headline {i + 1}: {headline}")
            print(f"Headline {i + 1}: {headline}")
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")  


#Logic to Rune Gemini API
def generate_text(prompt):
    # Initialize Vertex AI client
    aiplatform.init(project='your-project-id', location='your-region')  # Replace with your project ID and region
    
    # Create or retrieve a deployed model
    endpoint = aiplatform.Endpoint(endpoint_name='your-endpoint-id')  # Replace with your endpoint ID
    
    response = endpoint.predict(instances=[{"prompt": prompt}])
    if response.predictions:
        generated_text = response.predictions[0]['generated_text']
        return generated_text
    else:
        return "Sorry, I couldn't generate the content."


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        
        
        #Logic for executing taskes based on command
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia","")
            reults = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(reults)
            speak(reults)
            
        #Logic to open websites 
        elif 'open' in query:
            # Extract the application name and open it
            app_name = query.replace("open", "").strip()
            if 'website' in query or 'com' in query:
                website = app_name.replace("website", "").strip()
                url = f"http://{website}.com"
                speak(f"Opening {website}")
                webbrowser.open(url)
            else:
                speak(f"Opening {app_name}")
                open_application(app_name)
                
                
        elif 'play music' in query:
            play_music()
        
        elif 'news' in query:
            get_news()    
            
        elif 'generate text' in query:
            speak("What do you want me to write about?")
            content_prompt = takeCommand().lower()
            if content_prompt != "None":
                generated_text = generate_text(content_prompt)
                speak(f"Here's what Gemini generated for the prompt: {content_prompt}")
                print(generated_text)
                speak(generated_text)
            
         # Add a condition to exit the loop if needed
        if 'exit' in query or 'quit' in query or 'stop' in query or 'good by' in query or 'goodby' in query:
            speak("Goodbye! Have a great day!")
            break
        
        
