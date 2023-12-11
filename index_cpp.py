from llama_cpp import Llama

# conda activate llama
# https://github.com/abetlen/llama-cpp-python
def llama_chat(prompt):
    
    llm = Llama(model_path="./models/mistral-7b-openorca.Q4_0.gguf",main_gpu=0,
            n_gpu_layers=1, n_ctx=4096)
    output = llm.create_completion(f"""<|im_start|>system
    You are a helpful chatbot.
    <|im_end|>
    <|im_start|>user
    {prompt}?<|im_end|>
    <|im_start|>assistant""", max_tokens=500,  stop=["<|im_end|>"], stream=True)
    return output

#create Llama model

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
        except Exception as e:
            print("Error occurred: ", e)
        prompt = str(input('Enter another prompt: '))
    else:
        print('User: '+prompt+'\n')
        print('System: Chatbot is shutdown')
        break

