from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import speech_recognition as sr
import pyttsx3
import pandas as pd
from subprocess import Popen, PIPE

import time
import json
from pathlib import Path
import uvicorn
import os

from pydub import AudioSegment
import io

from modules import google_api as api
from modules import llama
from modules.robot import robot_speak

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

class QuestionRequest(BaseModel):
    question: str
    mode: str  
    model: str
    timestamp: float
    chat_id: str

class ConversationSaveRequest(BaseModel):
    chat_id: str
    conversation: list

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

save_dir = 'conversations'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

@app.post("/ask/")
async def ask_question(request: QuestionRequest):
    try:
        response, response_time = robot_response(request.question, request.mode, request.model)
        
        file_path = os.path.join(save_dir, f"{request.chat_id}.json")
        
        conversation_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                conversation_data = data.get("conversation", [])

        conversation_data.append({
            "sender": "user",
            "message": request.question,
            "timestamp": request.timestamp,
        })
        
        conversation_data.append({
            "sender": "bot",
            "message": response,
            "timestamp": time.time(),
            "response_time": response_time
        })
        
        with open(file_path, "w") as f:
            json.dump({"conversation": conversation_data}, f, indent=2)

        return {"response": response, "response_time": response_time}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/new_chat")
async def new_chat():
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    chat_id = f"conversation_{timestamp}"
    return {"chat_id": chat_id}

@app.get("/get_history")
async def get_history():
    """Returns a list of all saved conversation file names."""
    try:
        files = [f for f in os.listdir(save_dir) if f.endswith('.json')]
        # sort file based on timestamp
        files.sort(key=lambda x: os.path.getmtime(os.path.join(save_dir, x)), reverse=True)
        return JSONResponse({"history": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_conversation/{chat_id}")
async def get_conversation(chat_id: str):
    """Returns the content of a specific conversation file."""
    file_path = os.path.join(save_dir, f"{chat_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        with open(file_path, 'r') as f:
            conversation_data = json.load(f)
        return JSONResponse(conversation_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save_conversation")
async def save_conversation_endpoint(request: ConversationSaveRequest):
    try:
        file_name = f"{request.chat_id}.json"
        file_path = os.path.join(save_dir, file_name)

        with open(file_path, "w") as f:
            json.dump({
                "chat_id": request.chat_id,
                "conversation": request.conversation
            }, f, indent=2)

        return {"success": True, "message": "Conversation saved successfully"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"File system error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@app.get("/models")
async def get_models():
    return JSONResponse({"online_models": online_models, "offline_models": offline_models})

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the index.html file."""
    return Path("static/index.html").read_text()

@app.post("/voice_record")
async def voice_record(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    audio_data = await file.read()

    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
    audio_segment.export("temp/temp_audio.wav", format="wav")

    with sr.AudioFile("temp/temp_audio.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google_cloud(audio)
    except sr.UnknownValueError:
        text = ""

    return {"recognized_text": text}

@app.delete("/delete_conversation/{chat_id}")
async def delete_conversation(chat_id: str):
    """Deletes a specific conversation file from the server."""
    file_path = os.path.join(save_dir, f"{chat_id}.json")
    print(f"Attempting to delete conversation file: {file_path}")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    try:
        os.remove(file_path)
        return {"success": True, "message": f"Conversation {chat_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)