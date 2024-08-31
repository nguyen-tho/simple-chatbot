import tkinter as tk
from tkinter import filedialog, messagebox
from llama_cpp import Llama
from index_cpp import llama_chat
import os

class LlamaChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Llama Chatbot")

        # Bind Ctrl+S to save_conversation
        self.root.bind('<Control-s>', self.save_conversation)
        # Bind Alt+F4 to show_message
        self.root.bind('<Alt-F4>', self.quit)
        # Bind Ctrl+O to open_conversation
        self.root.bind('<Control-o>', self.open_conversation)

        # Create menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Conversation", command=self.open_conversation)
        self.file_menu.add_command(label="Save Conversation", command=self.save_conversation)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

        
        self.answer_label = tk.Label(root, text="System's answer:")
        self.answer_label.grid(row=0, column=0, padx=10, pady=10)
        self.answer_value = tk.Text(root, height=200, width=100)
        self.answer_value.grid(row=0, column=1,padx=10, pady=10)
        
        self.prompt_label = tk.Label(root, text="Enter your prompt:")
        self.prompt_label.grid(row=1, column=0, padx=10, pady=10)
        self.prompt_entry = tk.Entry(root, width=100)
        self.prompt_entry.grid(row=1, column=1, padx=10, pady=10)
        self.prompt_btn = tk.Button(root, text='Enter', command=self.ask_question)
        self.prompt_btn.grid(row=1, column=2, padx=10, pady=10)
        

        # Add frame for output text and scrollbar
        

    def ask_question(self):
        prompt = self.prompt_entry.get()
        self.answer_value.insert(tk.END, f"User: {prompt}\n")
        try:   
            output = llama_chat(prompt)
            answer_text = ''.join([token["choices"][0]["text"] for token in output])
            self.answer_value.insert(tk.END, f"System: {answer_text}\n")
        except Exception as e:
            self.answer_value.insert(tk.END, f"Error occurred: {e}\n")

    def save_conversation(self, event=None):
        try:
            # Define the specific directory to save the files
            specific_directory = "conversation/"

            # Ask for the file name without specifying the directory
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

            if file_path:
                # Combine the specific directory with the file name
                full_path = os.path.join(specific_directory, os.path.basename(file_path))

                with open(full_path, "w") as file:
                    conversation = self.output_text.get(1.0, tk.END)
                    file.write(conversation)

                messagebox.showinfo("Save Conversation", f"Conversation saved successfully to {full_path}!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save conversation: {e}")

    def open_conversation(self, event=None):
        try:
            specific_directory = "conversation/"

            # Ask for the file name without specifying the directory
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

            if file_path:
                # Combine the specific directory with the file name
                full_path = os.path.join(specific_directory, os.path.basename(file_path))
                
                with open(full_path, "r") as file:
                    conversation = file.read()
                    self.output_text.delete(1.0, tk.END)  # Clear previous text
                    self.output_text.insert(tk.END, conversation)
                messagebox.showinfo("Open Conversation", "Conversation opened successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open conversation: {e}")

    def quit(self, event=None):
        messagebox.showinfo("Notice", "Are you sure to quit")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LlamaChatUI(root)
    root.mainloop()
