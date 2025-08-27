import speech_recognition as sr
import pyttsx3
from rich.console import Console
from rich.markdown import Markdown

# initialize text-to-speech engine
engine = pyttsx3.init()
# initialize speech recognition
recognizer = sr.Recognizer()

def print_markdown_terminal(markdown_string):
    console = Console()
    md = Markdown(markdown_string)
    console.print(md)

def robot_speak(robot_brain):
    print("Robot:")
    print_markdown_terminal(robot_brain)
    engine.say(robot_brain)
    engine.runAndWait()
    return