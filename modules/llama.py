from llama_cpp import Llama
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="data_src/.env")
openorca_model = os.getenv("OPEN_ORCA_PATH")
llama2_model = os.getenv("LLAMA_2_PATH")

def get_offline_model(model_name): #model name key
    if model_name == "Open-Orca-7B":
        return openorca_model
    elif model_name == "Llama-2-13B":
        return llama2_model
    else:
        raise ValueError(f"Unknown model name: {model_name}")

# conda activate llama
# https://github.com/abetlen/llama-cpp-python
def activate_llama_model(model_name = openorca_model):
    # Load the LLaMA model
    model = Llama(model_path= model_name,main_gpu=1,
            n_gpu_layers=40, n_ctx=512)
    return model

def llama_chat(prompt, model):
 
    llm = activate_llama_model(model_name=model)
    out = llm.create_completion(f"""<|im_start|>system
    You are a helpful chatbot.
    <|im_end|>
    <|im_start|>user
    {prompt}?<|im_end|>
    <|im_start|>assistant""", max_tokens=1000,  stop=["<|im_end|>"], stream=True)
    return out
        
        

def send_response(output):
    robot_brain=''
    for token in output:
        robot_brain += token["choices"][0]["text"]
    return robot_brain





#create Llama model
'''
prompt = ''
prompt = str(input('Enter the prompt: '))
while True:
    if prompt != 'quit':
        try:
            output = llama_chat(prompt)
            print('=========================================================================================================================================================================')
            print('User: '+prompt+'\n')
            print('System: ')
            for token in output:
                print(token["choices"][0]["text"], end='', flush=True)
            print('=========================================================================================================================================================================')
        except Exception as e:
            print("Error occurred: ", e)
        prompt = str(input('Enter another prompt: '))
    else:
        print('User: '+prompt+'\n')
        print('System: Chatbot is shutdown')
        break

'''