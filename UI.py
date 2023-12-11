import tkinter as tk
from llama_cpp import Llama
from index_cpp import llama_chat

class LlamaChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Llama Chatbot")

        self.prompt_label = tk.Label(root, text="Enter your prompt:")
        self.prompt_label.pack()

        self.prompt_entry = tk.Entry(root, width=100)
        self.prompt_entry.pack()
        self.answer_label = tk.Label(root,text= "System's answer:")
        self.answer_label.pack()
        self.output_text = tk.Text(root, height=20, width=100)
        self.output_text.pack()

        #self.llm = Llama(model_path="./models/mistral-7b-openorca.Q4_0.gguf", n_gpu_layers=0, n_ctx=4096)

        self.ask_button = tk.Button(root, text="Ask", command=self.ask_question)
        self.ask_button.pack()

        self.quit_button = tk.Button(root, text="Quit", command=self.root.destroy)
        self.quit_button.pack()

    def ask_question(self):
        prompt = self.prompt_entry.get()
        try:
            self.output_text.insert(tk.END, f"User: {prompt}")
            output = llama_chat(prompt)
            answer_text = ''.join([token["choices"][0]["text"] for token in output])
            self.output_text.delete(1.0, tk.END)  # Clear previous text
            
            self.output_text.insert(tk.END, f"\nSystem: {answer_text}")
        except Exception as e:
            self.output_text.delete(1.0, tk.END)  # Clear previous text
            self.output_text.insert(tk.END, f"Error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LlamaChatUI(root)
    root.mainloop()
