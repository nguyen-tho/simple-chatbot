import tkinter as tk
from tkinter import filedialog, messagebox
from llama_cpp import Llama
from index_cpp import llama_chat
import os

import socket

def is_connected():
    """Checks if the device is connected to the internet."""
    try:
        # Try to resolve a common hostname (Google's public DNS)
        socket.create_connection(("8.8.8.8", 53), timeout=5)  # Google DNS, port 53
        return True
    except OSError:
        pass # Handle potential exceptions like timeouts, host not found, etc.
    return False

class LlamaChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Llama Chatbot")

      
        # Bind Alt+F4 to quit
        self.root.bind('<Alt-F4>', self.quit)

        # Create menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

        
        self.answer_label = tk.Label(root, text="System's answer:")
        self.answer_label.grid(row=0, column=0, padx=10, pady=10)
        self.answer_value = tk.Text(root, height=20, width=100)
        self.answer_value.grid(row=0, column=1,padx=10, pady=10)
        
        self.mode_toggle = tk.Button(root,text='ONLINE MODE', bg='green', command=self.toggle_button) # default is online
        self.mode_toggle.grid(row=1, column=0, padx=10, pady=10)
        self.mode_toggle.is_on = True
        
        self.prompt_label = tk.Label(root, text="Enter your prompt:")
        self.prompt_label.grid(row=2, column=0, padx=10, pady=10)
        self.prompt_entry = tk.Entry(root, width=100)
        self.prompt_entry.grid(row=2, column=1, padx=10, pady=10)
         # Insert placeholder text and set color
        self.prompt_entry.insert(0, "Enter text here...")
        self.prompt_entry.config(fg="grey")

        # Bind events for placeholder functionality
        self.prompt_entry.bind("<FocusIn>", self.on_entry_click)
        self.prompt_entry.bind("<FocusOut>", self.on_focus_out)
        
        self.prompt_btn = tk.Button(root, text='Enter', command=self.ask_question)
        self.prompt_btn.grid(row=2, column=2, padx=10, pady=10)
        

        # Add frame for output text and scrollbar
    
    
    def on_entry_click(self, event):
        if self.prompt_entry.get() == "Enter text here...":
            self.prompt_entry.delete(0, tk.END)
            self.prompt_entry.config(fg="black")  # Change text color

    def on_focus_out(self, event):
        if not self.prompt_entry.get():
            self.prompt_entry.insert(0, "Enter text here...")
            self.prompt_entry.config(fg="grey") # Change text color  
            
    def set_offline(self):
        self.mode_toggle.config(text="OFFLINE MODE", bg="red")
        self.mode_toggle.is_on = False

    def set_online(self):
        self.mode_toggle.config(text="ONLINE MODE", bg="green")
        self.mode_toggle.is_on = True 
        
    def toggle_button(self):
        if self.mode_toggle.is_on:  # Currently offline
            if not is_connected(): #check internet
                messagebox.showerror(title='Connection Error!!', message="No Internet Connection. Please turn on the Internet or use offline mode")
                self.set_offline()    
            else:
                self.set_offline() #also set offline if the button is currently online mode
        else:  # Currently offline
            if is_connected():
                self.set_online()
            else:
                messagebox.showerror(title='Connection Error!!', message="No Internet Connection. Please turn on the Internet or use offline mode")
                self.set_offline()

    def ask_question(self):
        prompt = self.prompt_entry.get()
        self.answer_value.insert(tk.END, f"User: {prompt}\n")
        try:   
            output = llama_chat(prompt)
            answer_text = ''.join([token["choices"][0]["text"] for token in output])
            self.answer_value.insert(tk.END, f"System: {answer_text}\n")
        except Exception as e:
            self.answer_value.insert(tk.END, f"Error occurred: {e}\n")

    def quit(self, event=None):
        messagebox.showinfo("Notice", "Are you sure to quit")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LlamaChatUI(root)
    root.mainloop()
