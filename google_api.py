import google.generativeai as genai
def get_api_key():
    with open('key.txt', 'r') as file:
        key = file.read()
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