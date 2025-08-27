import tkinter as tk
from tkinter import filedialog, messagebox
import modules.llama as llama
import os
import json
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



class LlamaChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Llama Chatbot")

        self.root.bind('<Alt-F4>', self.quit)  # Bind Alt+F4 to quit

        self.create_menu()
        self.create_widgets()
        self.load_models()
        self.configure_grid()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

    def create_widgets(self):
        # Answer area
        self.answer_label = tk.Label(self.root, text="System's answer:")
        self.answer_label.grid(row=0, column=0, padx=1, pady=1, sticky="nw")

        self.answer_value = tk.Text(self.root, height=10, width=100)
        self.answer_value.grid(row=0, column=1, columnspan=2, padx=1, pady=1, sticky="we")

        self.chatbot_speaker = tk.Button(self.root, text='Speaker', command=self.speaker_activation)
        self.chatbot_speaker.grid(row=0, column=3, padx=1, pady=1, sticky="w")

        # Mode toggle
        self.mode_toggle = tk.Button(self.root, text='OFFLINE', bg='red', command=self.toggle_button)
        self.mode_toggle.grid(row=1, column=3, padx=1, pady=1, sticky="w")
        self.mode_toggle.is_on = False

        # Model selection
        self.model_label = tk.Label(self.root, text='Choose model')
        self.model_label.grid(row=1, column=0, padx=1, pady=1, sticky="w")


        self.model_listbox = tk.Listbox(self.root, width=100, height=1, selectmode=tk.SINGLE, exportselection=False) #Crucial
        self.model_listbox.grid(row=1, column=1, padx=2, pady=2, sticky="we")

        self.model_scrollbar = tk.Scrollbar(self.model_listbox, command=self.model_listbox.yview)
        self.model_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.model_listbox.config(yscrollcommand=self.model_scrollbar.set)

        self.model_listbox.place_forget() #Initial hide

        self.select_button = tk.Button(self.root, text="Select Model", command=self.toggle_model_listbox)
        self.select_button.grid(row=1, column=2, padx=2, pady=2, sticky="w")

        # Prompt input
        self.prompt_label = tk.Label(self.root, text="Enter your prompt:")
        self.prompt_label.grid(row=2, column=0, padx=1, pady=1, sticky="w")

        self.prompt_entry = tk.Entry(self.root, width=100)
        self.prompt_entry.grid(row=2, column=1, padx=1, pady=1, sticky="we")
        self.prompt_entry.insert(0, "Enter text here...")
        self.prompt_entry.config(fg="grey")
        self.prompt_entry.bind("<FocusIn>", self.on_entry_click)
        self.prompt_entry.bind("<FocusOut>", self.on_focus_out)
        self.root.bind("<Button-1>", self.on_outside_click)

        self.prompt_btn = tk.Button(self.root, text='Enter', command=self.ask_question)
        self.prompt_btn.grid(row=2, column=2, padx=1, pady=1, sticky="w")

    def configure_grid(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def ask_question(self):
        # Placeholder for question asking logic
        question = self.prompt_entry.get()
        print(f"Question: {question}")
        self.answer_value.delete("1.0", tk.END)
        self.answer_value.insert(tk.END, "Answer from model...") #replace with model output.
    
        
    def on_entry_click(self, event):
        if self.prompt_entry.get() == "Enter text here...":
            self.prompt_entry.delete(0, tk.END)
            self.prompt_entry.config(fg="black")  # Change text color

    def on_focus_out(self, event):
        if not self.prompt_entry.get():
            self.prompt_entry.insert(0, "Enter text here...")
            self.prompt_entry.config(fg="grey") # Change text color  
            
    def set_offline(self):
        self.mode_toggle.config(text="OFFLINE", bg="red")
        self.mode_toggle.is_on = False

    def set_online(self):
        self.mode_toggle.config(text="ONLINE", bg="green")
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
                
        self.populate_listbox()
                
    def load_models(self):
        try:
            with open("api_key.json", "r") as f:
                self.models = json.load(f)
                print(self.models['online_model'])  # Debug
        except FileNotFoundError:
            self.models = {"online_model": [], "offline_model": []}  # Default empty models

    def populate_listbox(self):
        self.model_listbox.delete(0, tk.END)  # Clear existing items
        mode = self.mode_toggle.cget("text")
        self.model_listbox.delete(0, tk.END)  # Clear existing items
        if mode == "ONLINE":
            self.model_listbox.delete(0, tk.END)  # Clear existing items
            for model_data in self.models["online_model"]:
                print(model_data["name"])
                self.model_listbox.insert(tk.END, model_data["name"])
            #self.model_listbox.update_idletasks() # Force refresh
        elif mode == "OFFLINE":
            #self.model_listbox.delete(0, tk.END)  # Clear existing items
            for model_data in self.models["offline_model"]:
                self.model_listbox.insert(tk.END, model_data["name"])
                
        else:
            messagebox.showerror(title='Error', message="Invalid mode. Please select either online or offline mode")
            
    def speaker_activation(self):
        pass

    def ask_question(self):
        prompt = self.prompt_entry.get()
        self.answer_value.insert(tk.END, f"User: {prompt}\n")
        try:   
            output = llama.llama_chat(prompt)
            answer_text = ''.join([token["choices"][0]["text"] for token in output])
            self.answer_value.insert(tk.END, f"System: {answer_text}\n")
        except Exception as e:
            self.answer_value.insert(tk.END, f"Error occurred: {e}\n")

    def quit(self, event=None):
        messagebox.showinfo("Notice", "Are you sure to quit")
        self.root.destroy()
        
    def toggle_model_listbox(self):
        if self.model_listbox.winfo_ismapped():
            self.model_listbox.place_forget()
        else:
            self.model_listbox.place(in_=self.root, relx=0.1, rely=0.1, relwidth=0.4)
            self.model_listbox.lift()
            self.model_listbox.focus_set()

    def on_outside_click(self, event):
        if self.model_listbox.winfo_ismapped() and event.widget != self.model_listbox and event.widget != self.select_button:
            self.model_listbox.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = LlamaChatbot(root)
    root.mainloop()
