from datetime import datetime
import sys

def date_time():
   now = datetime.today()
   return now.strftime("%H : %M : %S")

def today():
    date = datetime.today()
    return date.strftime("%B %d %Y")

def how_are_you():
    return  "I am doing well, thank you for asking."

def good_bye():
    return "Good bye! It was nice talking to you!"

def greeting():
    current_time = datetime.now()
    hour = current_time.hour

    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    elif hour < 22:
        return "Good evening"
    else:
        return "Good night"
    
def name():
    return "My name is LLM chatbot. I am here to assist you."

def main():
    if len(sys.argv) != 2:
        print("Usage: python common.py <function_name>")
        sys.exit(1)
    
    function_name = sys.argv[1]

    # Create a dictionary mapping function names (strings) to the actual functions
    function_map = {
        "today": today,
        "date_time": date_time,
        "how_are_you": how_are_you,
        "good_bye": good_bye,
        "greeting": greeting,
        "name": name
    }

    # Get the function from the map, or None if it doesn't exist
    func = function_map.get(function_name)

    if func:
        # If the function exists in the map, call it
        print(func())
    else:
        # Otherwise, it's an invalid function name
        print("Invalid function name")

if __name__ == "__main__":
    main()