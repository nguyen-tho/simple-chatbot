import google.generativeai as genai
from dotenv import load_dotenv
import os

#load env
load_dotenv(dotenv_path="data_src/.env")

def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    return key
        
def call_api(api_key):
    # Create a client instance
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

def generate_response(model, prompt):
    response = model.generate_content(prompt)
    text = response.text
    return text