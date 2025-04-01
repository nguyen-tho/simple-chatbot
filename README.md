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
   create your Gemini API key and copy it to this file:
   ```sh
   key.txt
   ```
   Run program by app.py
   ```sh
   python app.py
   ```
3. New update
   - Build an API using Fast API (in process)
   - Build a simple web UI using HTML, CSS, and JS  
4. Contact:

    Please contact with me at this email address to discuss: nguyencongtho116@gmail.com
