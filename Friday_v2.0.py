#Friday v1.0
#Developer : Shahad
#Day 10/11/12


#import
import random
import datetime
import webbrowser
import tkinter as tk
import json
import pyttsx3
import threading
import os



#Speak Functions
def speak(text):
    def run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 165)

            voices = engine.getProperty('voices')
            female_voice = None

            for voice in voices:
                if "zira" in voice.name.lower() or "female" in voice.name.lower():
                    female_voice = voice.id
                    break

                if female_voice:
                    engine.setProperty('voice', female_voice)
                elif len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)

                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print("Audio Error:", e)
    threading.Thread(target=run, daemon=True).start()


#Memory Functions
memory={}
def load_memory():
    if not os.path.exists("memory.json"):
        print("--- Setup You Memory ---")
        name = input("Enter your name: ")
        age = input("Enter your age: ")
        city = input("Enter your city: ")
        hobby = input("Enter your hobby: ")

        user_data = {
            "name": name,
            "age": age,
            "city": city,
            "hobby": hobby
        }

        with open("memory.json", "w") as file:
            json.dump(user_data, file, indent=4)
        return user_data
    
    with open("memory.json", "r") as file:
        return json.load(file)
    
memory = load_memory()


secret_number = random.randint(1,10)


#Chat Functions
def chat():
    message = str(chat_entry.get()).strip().lower()
    print("Message =", repr(message))

    if not message:
        return
    
    chat_history.insert(tk.END, "You: " + message + "\n")

    user_name = memory.get("name", "friend")
    user_age = str(memory.get("age", "N/A"))
    user_city = memory.get("city", "your city")
    user_hobby = memory.get("hobby", "your hobbies")

    if message == "hi":
        response = "Hello!"
    elif message == "hey":
        response = "Hey!"
    elif message == "hello":
        response = f"Welcome back, {user_name}!"

    elif message in ["what is my name", "what's my name", " who am i", "tell me my name"]:
        response = f"Your name is {user_name}!"

    elif message in ["how old am i", "what is my age", "how old are you", "tell me my age"]:
        response = f"Your are {user_age}."

    elif message in ["where do i live", "what is my city", "tell me the city i live in"]:
        response = f"You live in {user_city}."

    elif message in ["what is my hobby", "what do i like" , "what do i enjoy", "tell me my hobby"]:
        response = f"Your hobby is {user_hobby}."


    elif message == "how are you":
        response = "I'm doing great!"

    elif message == "what's your name?":
        response = "My name is Friday!"
    
    elif  message == "who are you":
        response = "I'm Friday, an AI assistant."

    elif message == "how old are you":
        response = "I'm still growing and learning!"

    elif message == "bye":
        response = "Goodbye!"
    else:
        response = "I don't understand."

    result_label.config(text=response)
    chat_history.insert(tk.END, f"Friday: {response}\n")
    speak(response)
    chat_entry.delete(0, tk.END)


def talk(name, hobby, age):
    mood = input("How are you today? ")
    if mood == "fine":
        print("That's good to hear! ")
    elif mood == "sad":
        print("You told me your age is", age, " how about talking about your interests?" )
        print("I'm sorry to hear that. ")
    else:
        print("I remember your hobby is ", hobby)
        print("Thank you for telling me. ")


#Calculator
def calculator():
    num1 = int(number1.get())
    num2 = int(number2.get())
    answer = num1 + num2
    result_label.config(text="Answer: " + str(answer))


#Jokes
def joke():
    jokes=[
        "Why did the computer go to the doctor? Becuase it caught a viruse!",
        "Why do pragrammers loves python? Becuase it's easy to read!",
        "Why was the computer cold? It forget to close windows!",
        "Debugging: Being the detective in a crime movie where you're also the criminal."
    ]
    result_label.config(text=random.choice(jokes))


#Time & Date
def show_time():
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    result_label.config(text="Current Time: " + time)


def show_date():
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    result_label.config(text="Current Date: " + date)


#Websites
def open_google():
    webbrowser.open("https://www.google.com")

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def open_chatgpt():
    webbrowser.open("https://chat.openai.com")
    
def get_user_info():
    name = input("What is your name? ")
    age = input("How old are you? ")
    city = input("Which city do you live in? ")
    hobby = input("What is your hobby? ")
    return name, age, city, hobby

#Games
def game():
    global secret_number

    try:
        guess = int(chat_entry.get())

        if guess == secret_number:
            result_label.config(text="Correct!")

            chat_history.insert(
                tk.END,
                "Friday: Correct!\n"
            )

            secret_number = random.randint(1,10)
        else:
            result_label.config(text="Wrong, try again.")

            chat_history.insert(
                tk.END,
                "Friday:Wrong, try again.\n"
            )

    except:
        result_label.config(text="Please enter a number.")
    chat_entry.delete(0, tk.END)


def show_user_info(name, age, city, hobby):
    print("\n==== Your Information ====")
    print("Name:", name)
    print("Age:", age)
    print("City:", city)
    print("Hobby:", hobby)
    


def greeting(name):
    messages = [
        "Welcome back, " + name +"!",
        "Good to see you again, " + name + "!",
        "Hello, " + name + "! What shall we do today?",
        "Welcome back, " + name + "! I've been waiting for you.",
        "Hi, " + name + "! Let's build something amazing together.",
        "Ready to assist you, " + name + "! What can I do for you today?",
    ]
    print(random.choice(messages))
    print("Welcome back ", memory["name"])


#GUI
window = tk.Tk()
window.title("Friday v1.0")
window.geometry("600x950")


#Widgets
#Labels
Label = tk.Label(
    window,
    text="Friday AI Assistant",
    font=("Arial", 16),
)
Label.pack(pady=10)

subtitle = tk.Label(
    window,
    text="Choose what you want me to do. ",
    font=("Arial", 12)
)
subtitle.pack(pady=5)


#Buttons
google_button = tk.Button(
    window,
    text="Open Google",
    command=open_google,
)
google_button.pack(pady=5)

youtube_button = tk.Button(
    window,
    text="Open Youtube",
    command=open_youtube
)
youtube_button.pack(pady=5)

chatgpt_button= tk.Button(
    window,
    text="Open ChatGPT",
    command=open_chatgpt
)
chatgpt_button.pack(pady=5)

calculator_button = tk.Button(
    window,
    text="Calculator",
    command=calculator,
)
calculator_button.pack(pady=3)

joke_button = tk.Button(
    window,
    text="Tell me a joke",
    command=joke,
)
joke_button.pack(pady=3)

chat_button = tk.Button(
    window,
    text="Chat",
    command=chat,
)
chat_button.pack(pady=3)

game_button  = tk.Button(
    window,
    text="Guess Number",
    command=game
)
game_button.pack(pady=3)

time_button = tk.Button(
    window,
    text="Current Time",
    command=show_time,
)
time_button.pack(pady=3)

date_button = tk.Button(
    window,
    text="Today's Date",
    command=show_date
)
date_button.pack(pady=3)


#Entries
number1  = tk.Entry(window)
number1.pack(pady=3)

number2 = tk.Entry(window)
number2.pack(pady=3)


#Labels for Results
result_label = tk.Label(
    window,
    text="Answer will appear here.",
    font=("Arial", 12)
)
result_label.pack(pady=5)



#Text & Chat Area
chat_history = tk.Text(
    window,
    height=10,
    width=40
)
chat_history.pack(pady=5)

chat_entry = tk.Entry(
    window,
    width=30
)
chat_entry.pack(pady=3)

chat_label = tk.Label(
    window,
    text="Friday is waiting...",
    font=("Arial", 12)
)
chat_label.pack(pady=3)


#Main Treminal Flow & Loop
name = memory.get("name" , "User")
age = memory.get("age", "N/A")
city = memory.get("city", "N/A")
hobby = memory.get("hobby", "N/A")


show_user_info(name, age, city, hobby)

greeting(name)
print("Hello!, I am Friday.")

print("\nWhat do you want to do? ")
print("1. Talk")
print("2. Calculator")
print("3. Joke")
print("4. Time")
print("5. Date")
print("6. Open Google")
print("7. Open YouTube")
print("8. Open ChatGPT")
print("9. game")
print("10. Exit")
print("11. My Information")

choice = input("Choose a number: ")
if choice == "1":
    talk(name, hobby, age)
elif choice == "2":
    calculator()
elif choice == "3":
    joke()
elif choice == "4":
    show_time()
elif choice == "5":
    show_date()
elif choice == "6":
    open_google()
elif choice == "7":
    open_youtube()
elif choice == "8":
    open_chatgpt()
elif choice =="9":
    print("Please play the game inside the chat interface after the window open.")
elif choice == "10":
    print("Goodbye!")
elif choice == "11":
    print("\n==== Your Information ====")
    print("Name:", memory["name"])
    print("Age:", memory["age"])
    print("City:", memory["city"])
    print("Hobby:", memory["hobby"])

else:
    print("I don't understand.")


window.mainloop()