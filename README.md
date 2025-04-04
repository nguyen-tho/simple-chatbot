# simple-chatbot
A simple chatbot with Llama_cpp library and Mistral 7B Open Orca model

New update for this voice chatbot:
- Offline mode is Mistral 7B Open Orca model + Llama_cpp
- Online mode is Google Gemini API
1. References
   - Llama_cpp and chatgpt local:  https://github.com/conanak99/sample-gpt-local/tree/master
   - Voice chatbot: https://github.com/nguyen-tho/python-chatbot
   - Please get your Gemini API key in this URL: https://aistudio.google.com/apikey
2. How to use

   Setup environment by virtual environment (virtualenv or venv)
   ```sh
   python -m virtualenv <path to setup environment directory>
   ```
   Activate virtual environment
   ```sh
   # move to envinronment directory
   cd <path to directory>
   # activate environment
   source ./Scripts/activate
   ```
   Install necessary modules
   ```sh
   pip install -r requirements.txt
   ```
   create your Gemini API key and copy it to api_key.json at model Gemini:
   ```sh
   # api_key.json
   # with online models you add your api key to "api_key" field
   {
    "online_model":
    [
        {
            "model": "gemini-1.5-flash",
            "name": "Gemini 1.5 Flash",
            "api_key": "" #your api key

        }
   ]
   #with offline models you need to download models file with .gguf format (you can download it on hugging face)
   #copy the path to .gguf model file to "path" field
   "offline_model":
    [
        {
            "model":"Open-Orca-7B",
            "name": "Open Orca 7B",
            "path": "" #path to your .gguf file
        }
   ]
   ```
   Run program by terminal_app.py
   ```sh
   #run the simple chatbot on your terminal
   python terminal_app.py
   ```
   Run API
   ```sh
   #the API can run with localhost (127.0.0.1:80)
   #run app.py to run API
   python app.py
   ```
4. New update
   - Build an API using Fast API (in process)
   - Build a simple web UI using HTML, CSS, and JS  
5. Contact:

    Please contact with me at this email address to discuss: nguyencongtho116@gmail.com
