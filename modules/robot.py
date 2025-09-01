import speech_recognition as sr
import pyttsx3
from rich.console import Console
from rich.markdown import Markdown
import pandas as pd
from subprocess import Popen, PIPE
import time
import json

from modules import llama
from modules import google_api as api

def load_models(model_data_file="data_src/model.json"):
    try:
        with open(model_data_file, 'r') as f:
            model_data = json.load(f)

        online_models = {
            model["model"]: model["name"]
            for model in model_data.get("online_model", [])
        }

        offline_models = {
            model["model"]: model["name"]
            for model in model_data.get("offline_model", [])
        }

        return online_models, offline_models

    except FileNotFoundError:
        print(f"Error: Model data file '{model_data_file}' not found.")
        return {}, {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{model_data_file}'.")
        return {}, {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}, {}

online_models, offline_models = load_models()

# initialize text-to-speech engine
engine = pyttsx3.init()
# initialize speech recognition
recognizer = sr.Recognizer()

def print_markdown_terminal(markdown_string):
    console = Console()
    md = Markdown(markdown_string)
    console.print(md)

def robot_speak(robot_brain):
    print("Robot:")
    print_markdown_terminal(robot_brain)
    engine.say(robot_brain)
    engine.runAndWait()
    return

def common_question(question):
    data = pd.read_csv('data_src/common.csv')
    question = question.lower()

    direct_match = data[data['Question'].str.lower() == question]
    if not direct_match.empty:
        command = direct_match['Command'].values[0]
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        return str(output.decode("utf-8").strip())

    keyword_match = data[data['Keyword'].apply(lambda x: x.lower() in question)]
    if not keyword_match.empty:
        command = keyword_match['Command'].values[0]
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        output = process.communicate()[0]
        return str(output.decode("utf-8").strip())
    return None


def generate_response(prompt, mode, model):
    response = 'OK, Please wait ...\n'
    robot_speak(response)
    start_time = time.time()

    if mode == 'online' or mode == 'on':
        if model in online_models:
            key = api.get_api_key()
            api_model = api.call_api(key)
            response = api.generate_response(api_model, prompt)
        else:
            response = "Invalid online model selected."

    elif mode == 'offline' or mode == 'off':
        if model in offline_models:
            output = llama.llama_chat(prompt, model=llama.get_offline_model(model))
            response = llama.send_response(output)
        else:
            response = "Invalid offline model selected."
    else:
        response = 'Invalid mode. Please choose online or offline mode.\n'
    
    end_time = time.time()
    response_time = end_time - start_time
    
    robot_speak(response)
    return response, response_time

def robot_response(you, mode, model):
    data = pd.read_csv('data_src/common.csv')
    keyword = data[data['Keyword'].apply(lambda x: x.lower() in you)]
    response_time = 0

    if not keyword.empty:
        robot_brain = common_question(you)
        if robot_brain is not None:
            robot_speak(robot_brain)
            return robot_brain, response_time
        else:
            return generate_response(you, mode, model)
    else:
        return generate_response(you, mode, model)