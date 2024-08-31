from llama_cpp import Llama

# conda activate llama
# https://github.com/abetlen/llama-cpp-python
def llama_chat(prompt):
 
    llm = Llama(model_path="models\mistral-7b-openorca.Q4_0.gguf",main_gpu=0,
            n_gpu_layers=40, n_ctx=512)
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