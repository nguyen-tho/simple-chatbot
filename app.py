from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import speech_recognition
import pyttsx3
import pandas as pd
from subprocess import Popen, PIPE
from rich.console import Console
from rich.markdown import Markdown
import google_api as api
import index_cpp as llama
import time
import json
from pathlib import Path
import uvicorn

app = FastAPI()

robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

class QuestionRequest(BaseModel):
    question: str
    mode: str  
    model: str 

def load_models(model_data_file="api_key.json"):
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

def print_markdown_terminal(markdown_string):
    console = Console()
    md = Markdown(markdown_string)
    console.print(md)

def common_question(question):
    data = pd.read_csv('common.csv')
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

def robot_speak(robot_brain):
    print("Robot:")
    print_markdown_terminal(robot_brain)
    robot_mouth.say(robot_brain)
    robot_mouth.runAndWait()
    return

def generate_response(prompt, mode, model):
    response = 'OK, Please wait ...\n'
    robot_speak(response)

    if mode == 'online' or mode == 'on':
        if model in online_models:
            key = api.get_api_key()
            api_model = api.call_api(key)
            response = api.generate_response(api_model, prompt)
        else:
            response = "Invalid online model selected."

    elif mode == 'offline' or mode == 'off':
        if model in offline_models:
            llama_model = llama.get_llama_model()
            output = llama.llama_chat(prompt)
            response = llama.send_response(output)
        else:
            response = "Invalid offline model selected."
    else:
        response = 'Invalid mode. Please choose online or offline mode.\n'
    # robot_speak(response)
    return response

def robot_response(you, mode, model):
    data = pd.read_csv('common.csv')
    keyword = data[data['Keyword'].apply(lambda x: x.lower() in you)]

    if not keyword.empty:
        robot_brain = common_question(you)
        if robot_brain is not None:
            #robot_speak(robot_brain)
            return robot_brain
        else:
            return generate_response(you, mode, model)
    else:
        return generate_response(you, mode, model)

@app.post("/ask/")
async def ask_question(request: QuestionRequest):
    try:
        response = robot_response(request.question, request.mode, request.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
@app.post("/speak/")
async def speak_question(request: QuestionRequest):
    try:
        robot_mouth.say("Please speak your question.")
        robot_mouth.runAndWait()
        with speech_recognition.Microphone() as mic:
            print("Robot: I'm Listening\n", end='', flush=True)
            audio = robot_ear.listen(mic)
            print("Robot:...")
        you = robot_ear.recognize_google_cloud(audio)
        print("User: " + you)
        response = robot_response(you, request.mode, request.model)
        return {"response": response}
    except speech_recognition.UnknownValueError:
        return {"response": "Could not understand audio"}
    except speech_recognition.RequestError as e:
        return {"response": f"Could not request results from Google Cloud Speech Recognition service; {e}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
@app.get("/models")
async def get_models():
    return JSONResponse({"online_models": online_models, "offline_models": offline_models})

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the index.html file."""
    return Path("static/index.html").read_text()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)