import speech_recognition
import pyttsx3
#import gtts
import os

from subprocess import PIPE, Popen
import index_cpp
import subprocess
import pandas as pd
    
robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()

def common_question(question):
    data = pd.read_csv('common.csv')
    question = question.lower()

    # Check if the question directly matches any row in the dataset
    direct_match = data[data['Question'].str.lower() == question]
    if not direct_match.empty:
        command = direct_match['Command'].values[0]
        #print(command)
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        return str(output.decode("utf-8").strip())

    # Check if any keyword in the question matches the 'Keyword' column in the dataset
    keyword_match = data[data['Keyword'].apply(lambda x: x.lower() in question)]
    if not keyword_match.empty:
        command = keyword_match['Command'].values[0]  # Fix: Use keyword_match instead of direct_match
        #print(command)
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        return str(output.decode("utf-8").strip())

def robot_answer(robot_brain):
    print("Robot:" + robot_brain)
    robot_mouth.say(robot_brain)
    robot_mouth.runAndWait()
    return

while True: 
    robot_mouth.say("I'm Listening")
    robot_mouth.runAndWait()
    with speech_recognition.Microphone() as mic:
        print("Robot: I'm Listening")
        audio = robot_ear.listen(mic)    
    print("Robot:...") 
    try:
        you = robot_ear.recognize_google_cloud(audio)
        print("User: " + you)
    except:
        you = ""

    #you = "how are you"
    print("You: "+you)
    if you == "":
        robot_brain = "I can't hear you, try again"
        robot_answer(robot_brain)
    elif  "how are you" in you or "time" in you or "today"  in you or "bye"  in you :
        robot_brain = common_question(you)
        robot_answer(robot_brain)
    else:
        chat_response = index_cpp.llama_chat(you)
        robot_brain = index_cpp.send_response(chat_response)
        robot_answer(robot_brain)
        
