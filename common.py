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
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    elif hour < 20:
        return "Good evening"
    else:
        return "Good night"


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python common.py <function_name>")
        sys.exit(1)

    function_name = sys.argv[1]
    if function_name == "today":
        print(today())
    elif function_name == "date_time":
        print(date_time())
    elif function_name ==  "how_are_you":
        print(how_are_you())
    elif function_name ==  "good_bye":
        print(good_bye())
   elif function_name == 'greeting':
        print(greeting())
   else:
        print("It is not included in the list")
