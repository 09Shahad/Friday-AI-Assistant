#Friday v4.0
#Developer : Shahad
#Day ~


#import
import random
import datetime
import webbrowser
import tkinter as tk
import json
import pyttsx3
import threading
import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq
from tkinter import scrolledtext
import speech_recognition as sr


load_dotenv(find_dotenv(), override=True)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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
        default_data = {
            "name": "Shahad",
            "age": "17",
            "city": "Ajman",
            "hobby": "Coding"
        }
        with open("memory.json", "w", encoding="utf-8") as file:
            json.dump(default_data, file, indent=4)
        return default_data

    with open("memory.json", "r", encoding="utf-8") as file:
       return json.load(file)

def save_memory():
    with open("memory.json", "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)

def update_memory(key, value):
    memory[key] = value
    save_memory()
    
memory = load_memory()


secret_number = random.randint(1,10)


#Chat Functions
def ask_ai(prompt):
    try:

        memory_context = "\n".join([f"- {k}: {v}" for k, v in memory.items()])

        system_instruction = (
            f"You are Friday, a concise and direct AI assistant. "
            f"Current user memory:\n{memory_context}\n\n"
            f"Instructions:\n"
            f"1. Keep all your responses short, natural, and straight to the point (1-2 sentences max). Avoid long explanations."
            f"2. If the user shares new personal facts, acknowledge it naturally."
        )

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=60
        )
        response_text = chat_completion.choices[0].message.content

        update_prompt = (
            f"Analyze this user message: '{prompt}'."
            f"If it contains a new personal detail or updates an existing one (like favorite color, new hobby, etc.),"
            f"output ONLY in this formate: key=value. Otherwise output NONE."
        )

        mem_check = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": update_prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=20
        ).choices[0].message.content.strip()

        if "=" in mem_check and "NONE" not in mem_check:
            key, val = mem_check.split("=", 1)
            update_memory(key.strip().lower(), val.strip())

        return response_text

    except Exception as e:
        return f"Error: {e}"


def check_web_commands(text):
    text = text.lower()

    if "youtube music" in text or "yt music" in text or "يويتوب ميوزك" in text:
        open_yt_music()
        return "Opening YouTube Music"
    elif "youtube" in text or "يوتيوب" in text:
        open_youtube()
        return "Opening YouTube"
    elif "google" in text or "جوجل" in text:
        open_google()
        return "Opening Google"
    elif "chatgpt" in text or "chat gpt" in text or "شات جي بي تي" in text:
        open_chatgpt()
        return "Opening ChatGPT"

    return None


def listen():
    global chat_display
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_label.config(text="Friday is listening...")
        window.update()
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en-US")
            chat_entry.delete(0, tk.END)
            chat_entry.insert(0, text)
            chat_label.config(text="Friday is waiting")

            web_response = check_web_commands(text)

            if web_response:
                chat_display.insert(tk.END, f"You: {text}\nFriday: {web_response}\n\n")
                chat_display.see(tk.END)
                speak(web_response)
            else:
                chat()

        except Exception:
            chat_label.config(text="Could not understand...")
            window.after(2000, lambda: chat_label.config(text="Friday is waiting"))


def start_listening():
    threading.Thread(target=listen, daemon=True).start()


def chat():
    message = str(chat_entry.get()).strip().lower()
    print("Message =", repr(message))

    if not message:
        return
    
    chat_history.insert(tk.END, "You: " + message + "\n")
    chat_entry.delete(0, tk.END)

    action_result = check_web_commands(message)\

    if action_result:
        response = action_result

    else:
        response = ask_ai(message)


    chat_history.insert(tk.END, f"Friday: {response}\n\n")
    chat_history.see(tk.END)
    speak(response)



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

def open_yt_music():
    webbrowser.open("https://music.youtube.com")

    


    
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
BG_COLOR = "#1E1E2E"
FRAME_BG = "#2B2B3B"
TEXT_FG = "#FFFFFF"
BTN_BG = "#3B4252"
BTN_FG = "#ECEFF4"
ACCENT_COLOR = "#88C0D0"

#Adjust the main window
window = tk.Tk()
window.title("Friday AI assistant")
window.geometry("520x750")
window.configure(bg=BG_COLOR)

#Labels
Label = tk.Label(
    window,
    text="Friday AI Assistant",
    font=("Segoe UI", 16, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
Label.pack(pady=(15,5))

subtitle = tk.Label(
    window,
    text="Choose what you want me to do:",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg="#D8DEE9"
)
subtitle.pack(pady=(0,10))

#Button Frame
button_frame = tk.Frame(window, bg=FRAME_BG, bd=1, relief="solid", padx=10, pady=10)
button_frame.pack(pady=5, padx=20)

#Hover Effect
def on_enter(e):
    e.widget['background'] = "#4C566A"

def on_leave(e):
    e.widget['background'] = BTN_BG

#Buttons Data
buttons_data = [
    ("Open Google", open_google, 0, 0),
    ("Open Youtube", open_youtube, 0, 1),
    ("Open ChatGPT", open_chatgpt, 1, 0),
    ("Calculator", calculator, 1, 1),
    ("Tell me a Joke", joke, 2, 0),
    ("Chat", chat, 2, 1),
    ("Guess Number", game, 3, 0),
    ("Current Time", show_time, 3, 1),
    ("Today's Date", show_date, 4, 0),
    ("YouTube Music", open_yt_music, 4, 1)
]

for text, cmd, r, c in buttons_data:
    btn = tk.Button(
        button_frame,
        text=text,
        command=cmd,
        font=("Segoe UI", 9, "bold"),
        bg=BTN_BG,
        fg=BTN_FG,
        activebackground="#5E81AC",
        activeforeground="#FFFFFF",
        relief="flat",
        width=18,
        pady=5
    )
    btn.grid(row=r, column=c, padx=5, pady=4)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

#Enters & Result
entries_frame = tk.Frame(window, bg=BG_COLOR)
entries_frame.pack(pady=5)

number1 = tk.Entry(entries_frame, width=12, font=("Segoe UI", 10), justify="center", bg="#2E3440", fg="#FFFFFF", insertbackground="white") 
number1.grid(row=0, column=0, padx=5)

number2 = tk.Entry(entries_frame, width=12 , font=("Segoe UI", 10), justify="center", bg="#2E3440", fg="#FFFFFF", insertbackground="white") 
number2.grid(row=0, column=1, padx=5)

result_label = tk.Label(
    window,
    text="Answer will appear here.",
    font=("Segoe UI", 11, "italic"),
    bg=BG_COLOR,
    fg="#E5E9F0"
)
result_label.pack(pady=8)

#Chat History & Input
chat_history = scrolledtext.ScrolledText(
    window,
    height=8,
    width=52,
    font=("Consolas", 10),
    bg="#2E3440",
    fg="#ECEFF4",
    relief="flat",
    padx=8,
    pady=8
)
chat_history.pack(pady=5)

chat_entry = tk.Entry(
    window,
    width=40,
    font=("Segoe UI", 10),
    bg="#2E3440",
    fg="#FFFFFF",
    insertbackground="white",
    relief="flat"
)
chat_entry.pack(pady=5)

mic_button = tk.Button(
    window,
    text="🎤 voice",
    font=("Segoe UI", 9, "bold"),
    bg="#4C566A",
    fg="#FFFFFF",
    command=start_listening,
)
mic_button.pack(pady=3)

chat_label = tk.Label(
    window,
    text="Friday is waiting",
    font=("Segoe UI", 10, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
chat_label.pack(pady=(2, 10))



#Main Flow 
name = memory.get("name", "User")
age = memory.get("age", "N/A")
city = memory.get("city", "N/A")
hobby = memory.get("hobby", "N/A")

show_user_info(name, age, city, hobby)
greeting(name)


window.mainloop()