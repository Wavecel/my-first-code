import speech_recognition as sr
import pyttsx3
import pyaudio
import pywhatkit
import datetime
import wikipedia
import subprocess
import re
import cv2 
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
rate = engine.getProperty('rate')
newrate=150
voices= engine.getProperty('voices')
engine.setProperty('voice',voices[2].id)
engine.setProperty('rate',newrate)
engine.say('hey there, I am your personal assistant !!')
engine.say('what can i do for you?')
engine.runAndWait()


def cam():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

def vivek():
    
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
    wifi_list = list()

    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = dict()
            
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile) 

    
    return(wifi_list)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("listening.....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis','')
                #talk(command)
    except:
        while True:
            take_command() 
    return command

def run_jarvis():
    command = take_command()
    print(command)
    if 'play' in command:
        song=command.replace('play','')
        print('playing..'+song)
        talk('playing, '+ song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time= datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('now the time is, ' + time)
    elif 'who is' in command:
        talk('searching..')
        info = command.replace('who is','')
        info = wikipedia.summary(info,3)
        talk(info)
        print(info) 
    elif 'who are you' in command:
        talk('Not yet decided but you will know about me by the end of 2024')
    elif'bye' in command:
        talk('bye!')
    elif'can you dance' in command:
        talk('have you gone mad i dont have a body ,, hmmmmmm lets think about this when i have a body thats so soon!!')
    elif "can you do" in command:
        talk('iam not fully developed. but, currently i can tell u time, search for a person, play songs on youtube')
    elif'wi-fi password' in command:
        talk('your wifi passwords are:')
        print(vivek())
        talk(vivek())
        
    elif 'open camera' in command:
        talk('oppening camera')
        cam()
    elif 'a joke' in command:
        joke=pyjokes.get_joke(language='en', category= 'neutral')
        print(joke)
        talk(joke)

    else:
        talk('sry, i didnt get you could you please say again')

while True:
    run_jarvis()

