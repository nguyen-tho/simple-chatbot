import speech_recognition
import pyttsx3
#import gtts
import os
from modules import google_api as api
from subprocess import PIPE, Popen
from modules import llama
import pandas as pd
import time

from modules.robot import robot_speak

    
robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()

def common_question(question):
    data = pd.read_csv('data_src/common.csv')
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
    

def generate_response(prompt):
    mode = input('Choose mode: ')
    response = 'OK, Please wait ...\n'
    robot_speak(response)
    if mode == 'online' or mode == 'on':
        key = api.get_api_key()
        model = api.call_api(key)
        response = api.generate_response(model, prompt)
        
    elif mode == 'offline' or mode == 'off':
        model = llama.get_llama_model()
        output = llama.llama_chat(prompt)
        response = llama.send_response(output)
    else:
        response = 'Invalid mode. Please choose online or offline mode.\n'
    
    robot_speak(response)
        
def robot_response(you):
    data = pd.read_csv('data_src/common.csv')
    keyword = data[data['Keyword'].apply(lambda x: x.lower() in you)]

    if not keyword.empty:# response common question in dataset
        robot_brain = common_question(you)
        robot_speak(robot_brain)
    else:# response by LLM model
        generate_response(you) 
 
while True:
    # user can choose to type or speak
    robot_speak("Do you want to type (t/1) or speak(s/2)?")
    choose = input("Type or Speak: ")
    if choose == 'type' or choose == 't' or choose == '1':# user type
        you = input("Type your question: ")
        robot_response(you)
    elif choose == 'speak' or choose == 's' or choose == '2':# user speak
        robot_speak("Please speak your question.")
        robot_mouth.say("I'm Listening")
        robot_mouth.runAndWait()
        with speech_recognition.Microphone() as mic:
            print("Robot: I'm Listening\n", end='', flush=True)
        audio = robot_ear.listen(mic)    
        print("Robot:...") 
   
        try:
            you = robot_ear.recognize_google_cloud(audio)
            print("User: " + you)
        except:
            you = ""

    #you = "how to learn java"
            print("You: "+you)
            attempt_count = 0
            while attempt_count < 3:
                if you == "":
                    if attempt_count < 2:
                        robot_brain = "I can't hear you, try again.\n"
                        robot_speak(robot_brain)
                        attempt_count += 1
                        time.sleep(3) # wait for 3 seconds
                    else:
                        robot_speak("I can't seem to understand your input. Please type your question.\n")
                        you = input("Type your question: ")
                else:
                    robot_response(you)
                    break
    if 'bye' in you:
        break # when good bye is said, the robot will stop listening, exit the loop and stop the program
    else:
        #if not people can ask something else
        robot_speak("Do you have any other questions?")
        continue