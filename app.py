# modules for app flow
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# modules for user security
#from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel
import speech_recognition as sr
import pyttsx3
import pandas as pd

#from sqlalchemy.orm import Session


import time
import json
from pathlib import Path
from datetime import datetime, timedelta

import uvicorn
import os

from pydub import AudioSegment
import io

from modules import google_api as api
from modules import llama
from modules.robot import robot_response, online_models, offline_models
#from modules.authentication import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
#from modules.database_connection import User, get_db

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
"""
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.password != form_data.password: # NOTE: This is a placeholder. You should use a secure password hashing method.
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
"""

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)