#Friday v4.0
#Developer : Shahad
#Day ~


#import
import random
from datetime import datetime, time, timedelta
import webbrowser
import tkinter as tk
import json
import threading
import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq
from tkinter import scrolledtext
import speech_recognition as sr
import subprocess
import pyautogui
import winsound
import time 
from tkinter import messagebox
import asyncio
import edge_tts
import pygame

pygame.mixer.init()

import requests
import xml.etree.ElementTree as ET


load_dotenv(find_dotenv(), override=True)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Speak Functions


def speak(text):
    def run():
        try:
            if "window" in globals():
                window.after(0, lambda: update_status("speaking"))

            async def _speak():
                VOICE = "en-US-JennyNeural"
                OUTPUT_FILE = "voice.mp3"

                communicate = edge_tts.Communicate(text, VOICE)
                await communicate.save(OUTPUT_FILE)

                pygame.mixer.init()
                pygame.mixer.music.load(OUTPUT_FILE)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()

            asyncio.run(_speak())

            if "window" in globals():
                window.after(0, lambda: update_status("idle"))

        except Exception as e:
            print("Audio Error:", e)
            if "window" in globals():
                window.after(0, lambda: update_status("idle"))

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
    user_msg = prompt.lower().strip()

    if "add task" in user_msg or "add to do" in user_msg or "add todo" in user_msg:
        task_text = prompt.split("to", 1)[-1].strip() if "to" in prompt else prompt
        return add_tasks(task_text)

    if "show tasks" in user_msg or "my tasks" in user_msg or "show my tasks" in user_msg or "get tasks" in user_msg:
        return get_tasks()

    if "remind me" in user_msg:
        try:
            parts = prompt.split("at")
            text = parts[0].replace("remind me to", "").replace("remind me", "").strip()
            time_str = parts[1].strip()
            return add_reminder_item(text, time_str)
        except Exception as e:
            return f"Error setting reminder: {e}"


    try:

        memory_context = "\n".join([f"- {k}: {v}" for k, v in memory.items()])

        system_instruction = (
            f"You are Friday, a concise and direct AI assistant. "
            f"Current user memory:\n{memory_context}\n\n"
            f"Instructions:\n"
            f"1. Keep all your responses short, natural, and straight to the point (1-2 sentences max). Avoid long explanations."
            f"2. If the user shares new personal facts, acknowledge it naturally."
        )

        PRIMARY_MODEL = "allam-2-7b"
        FALLBACK_MODEL = "allam-2-7b"

        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                model=PRIMARY_MODEL,
                max_tokens=60
            )
        except Exception:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                model=FALLBACK_MODEL,
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
            model=PRIMARY_MODEL,
            max_tokens=20
        ).choices[0].message.content.strip()

        if "=" in mem_check and "NONE" not in mem_check:
            key, val = mem_check.split("=", 1)
            update_memory(key.strip().lower(), val.strip())

        return response_text

    except Exception as e:
        return f"Error: {e}"


def start_timer_thread(seconds, message="Timer finished!"):
    def timer():
        time.sleep(seconds)
        for _ in range(3):
            winsound.Beep(1000, 500)
            time.sleep(0.2)

        try:
            speak(message)
        except Exception:
            pass

        from tkinter import messagebox
        messagebox.showinfo("Friday Reminder", message)

    threading.Thread(target=timer, daemon=True).start()


def save_note(note_text):
    with open("notes.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] {note_text}\n")
    return "Note saved successfully."

def read_notes():
    try:
        with open("notes.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return "You have no saved notes."
            return "Your notes: " + " | ".join([line.strip() for line in lines[-3:]])
    except FileNotFoundError:
        return "You have no saved notes."


def add_tasks(task, day="today"):
    day_key = datetime.now().strftime("%Y-%m-%d") if day == "today" else day.lower()

    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            date = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        date = {}

    if day_key not in date:
        date[day_key] = []

    date[day_key].append(task)

    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(date, f, ensure_ascii=False, indent=4)

    return f"Added '{task}' to your tasks for {day}."

def get_tasks(day="today"):
    day_key = datetime.now().strftime("%Y-%m-%d") if day == "today" else day.lower()

    try: 
        with open("tasks.json", "r", encoding="utf-8") as f:
            date = json.load(f)
            tasks = date.get(day_key, [])
            if not tasks:
                return f"You have no tasks for {day}."
            return f"Your tasks for {day}: " + " , ".join(tasks)
    except FileNotFoundError:
        return "No tasks saved yet."

import re

def add_reminder_item(text, time_str):
    match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', time_str, re.IGNORECASE)
    if not match:
        return "Please specify time format like '09:45 PM' or '21:45'."

    hours = int(match.group(1))
    minutes = int(match.group(2))
    period = match.group(3)

    if period:
        period = period.upper()
        if period =="PM" and hours < 12:
            hours += 12
        elif period == "AM" and hours == 12:
            hours = 0

    time_obj = datetime.strptime(f"{hours:02d}:{minutes:02d}", "%H:%M")
    formatted_time = time_obj.strftime("%I:%M %p")

    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if "reminders" not in data:
        data["reminders"] = []

    data["reminders"].append({"text":text, "time": formatted_time, "notified":False})

    with open("tasks.json", "w", encoding="utf=8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return f"Reminder set for '{text}' at {formatted_time}."
    


def check_reminders_loop():
    while True:
        now = datetime.now().strftime("%I:%M %p")
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            update = False
            for rem in data.get("reminders", []):
                if rem["time"] == now and not rem.get("notified", False):
                    rem ["notified"] = True
                    update = True
                    msg = f"Reminder: {rem['text']}"
                    speak(msg)
                    if "window" in globals():
                        window.after(0, lambda m=msg: messagebox.showinfo("Reminder, m"))

            if update:
                with open("tasks.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass
        time.sleep(30)


def take_screenshot():
    try:
        folder_name = "screenshots"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-&M-%S")
        file_path = os.path.join(folder_name, f"screenshots_{timestamp}.png")

        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)

        return True 
    except Exception as e:
        print("Screenshots Error:", e)
        return False



def check_web_commands(text):
    text = text.lower()

#Controlling volume level
    if "volume up" in text or "ارفعي الصوت" in text or " turn up" in text or "raise the volume" in text:
        import re
        numbers = re.findall(r'\d+', text)
        amount = int(numbers[0]) if numbers else 5

        for _ in range(amount):
            pyautogui.press("volumeup")
        return f"Raising volume by {amount}"

    elif "volume down" in text or "نقصي الصوت" in text:
        import re
        numbers = re.findall(r'\d+', text)
        amount = int(numbers[0]) if numbers else 5

        for _ in range(amount):
            pyautogui.press("volumedown")
        return f"Lowering volume by {amount}"

    elif "mute" in text or "كتم الصوت" in text:
        pyautogui.press("volumemute")
        return "Muting volume"

#open Apps 
    elif "open notepad" in text or "افتحي المفكرة" in text:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad"

    elif "open calculator" in text or "افتحي الآلة الحاسبة" in text:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator"

    elif "open paint" in text or "افتحي الرسام" in text:
        subprocess.Popen(["mspaint.exe"])
        return "Opening Paint"

#Searching on the web
    elif "search youtube for" in text or "ابحث في يوتيوب عن" in text:
        query = text.replace("search youtube for", "").replace("ابحث في يوتيوب عن", "").strip()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Searching YouTube for '{query}'"

    elif "search google for" in text or "ابحث في جوجل عن" in text or "ابحثي عن" in text:
        query = text.replace("search google for", "").replace("ابحث في جوجل عن", "").replace("ابحثي عن", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for '{query}'"

    elif "play song" in text or "play" in text or "شغلي أغنية" in text or "شغلي" in text or "search music for" in text or "ابحثي عن أغنية" in text:
        query = text.replace("play song", "").replace("play", "").replace("شغلي أغنية", "").replace("شغلي", "").replace("search music for", "").replace("ابحثي عن أغنية", "").strip()
        if query:
            webbrowser.open(f"https://music.youtube.com/search?q={query}")
            return f"Searching YouTube Music for '{query}'"
        else:
            open_yt_music()
            return "Opening YouTube Music"


#open websites
    elif "youtube music" in text or "yt music" in text or "يويتوب ميوزك" in text:
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


#Timer and Reminder
    elif "timer" in text or "set a timer" in text:
        import re
        numbers = re.findall(r'\d+', text)
        amount = int(numbers[0]) if numbers else 1

        if "second" in text or "seconds" in text or "ثانية" in text or "ثواني" in text:
            seconds = amount

        elif "hour" in text or "hours" in text or "ساعة" in text or "ساعات" in text:
            seconds = amount * 3600
        else:
            seconds = amount * 60

        msg = "Time is up!" if ("timer" in text or "set a timer" in text or "منبه" in text) else text
        start_timer_thread(seconds, msg)
        return f"Timer set for {amount} unit(s)."

#Write Notes
    elif "write note" in text or "اكتبي ملاحظة" in text or "اكتبي بالملاحظات" in text:
        note_content = text.replace("write note", "").replace("اكتبي ملاحظة", "").replace("اكتبي بالملاحظات", "").strip()
        if note_content:
            return save_note(note_content)
        return "What would you like me to note down?"

#Read Notes
    elif "show notes" in text or "read notes" in text or "اقرئي ملاحظاتي" in text or "الملاحظات" in text or "show note" in text:
        return read_notes()

    elif "add task" in text or "اضيفي مهمه" in text or "سجلي مهمه" in text:
        task = text.replace("add task", "").replace("اضيفي مهمه", "").replace("سجلي مهمه", "").strip()
        if task:
            return add_tasks(task, "today")
        return "what task do you want to add?"

    elif "show tasks" in text or "my tasks" in text or "جدول اليوم" in text or "شو عندي اليوم" in text:
        return get_tasks("today")

#weather 
    elif any(k in text for k in ["weather", "weather today", "كيف الجو", "الطقس"]):
        import requests
        try:
            city = "Ajman"
            url = f"https://wttr.in/{city}?format=%C+%t"
            response = requests.get(url)
            if response.status_code == 200:
                weather_date = response.text.strip()
                return f"The weather in {city} is currently {weather_date}."
            return "Sorry, I couldn't fetch the weather right now."
        except Exception:
            return "Unable to connect to the weather service."

#News
    elif any(k in text for k in ["news", "letest news", "الأخبار"]):
        import requests
        import xml.etree.ElementTree as ET
        try:
            url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
            response = requests.get(url)
            root = ET.fromstring(response.content)

            headlines = []
            for item in root.findall('.//item')[:3]:
                headlines.append(item.find('title').text)

            return "Here are the top headlines: " + " | ".join(headlines)
        except Exception:
            return "sorry. I coudn't retrieve the news at the moment."

  
    elif any( k in text.lower() for k in ["screenshot", "take screenshot", "صوري الشاشة", "لقطة الشاشة"]):
        if take_screenshot():
            return "Screenshot saved successfully."
        else:
            return "Sorry, I could not take a screenshot."

        
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

            chat_history.insert(tk.END, f"You: {text}\n")

            web_response = check_web_commands(text)

            if web_response:
                response = web_response
            else:
                response = ask_ai(text)

            chat_history.insert(tk.END, f"Friday: {response}\n\n")
            chat_history.see(tk.END)
            speak(response)

        except Exception as e:
            print("Error in listening:", e)
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

#Scrollbar Setup
main_canvas = tk.Canvas(window, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg=BG_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

main_canvas.bind(
    "<Configure>",
    lambda e: main_canvas.itemconfig(canvas_window, width=e.width)
)

main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

window.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

#Labels
Label = tk.Label(
    scrollable_frame,
    text="Friday AI Assistant",
    font=("Segoe UI", 16, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
Label.pack(pady=(15,5))

subtitle = tk.Label(
    scrollable_frame,
    text="Choose what you want me to do:",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg="#D8DEE9"
)
subtitle.pack(pady=(0,10))

#Button Frame
button_frame = tk.Frame(scrollable_frame, bg=FRAME_BG, bd=1, relief="solid", padx=10, pady=10)
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
entries_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
entries_frame.pack(pady=5)

number1 = tk.Entry(entries_frame, width=12, font=("Segoe UI", 10), justify="center", bg="#2E3440", fg="#FFFFFF", insertbackground="white") 
number1.grid(row=0, column=0, padx=5)

number2 = tk.Entry(entries_frame, width=12 , font=("Segoe UI", 10), justify="center", bg="#2E3440", fg="#FFFFFF", insertbackground="white") 
number2.grid(row=0, column=1, padx=5)

result_label = tk.Label(
    scrollable_frame,
    text="Answer will appear here.",
    font=("Segoe UI", 11, "italic"),
    bg=BG_COLOR,
    fg="#E5E9F0"
)
result_label.pack(pady=8)

#Chat History & Input
chat_history = scrolledtext.ScrolledText(
    scrollable_frame,
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
    scrollable_frame,
    width=40,
    font=("Segoe UI", 10),
    bg="#2E3440",
    fg="#FFFFFF",
    insertbackground="white",
    relief="flat"
)
chat_entry.pack(pady=5)

# Canvas Circle
status_canvas = tk.Canvas(scrollable_frame, width=70, height=70, bg=BG_COLOR, highlightthickness=0)
status_canvas.pack(pady=5)
status_circle = status_canvas.create_oval(10, 10, 60, 60, fill="#4A5568", outline=ACCENT_COLOR, width=2)

chat_label = tk.Label(
    scrollable_frame,
    text="Friday is waiting",
    font=("Segoe UI", 10, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
chat_label.pack(pady=(2, 5))


#Update Status Function
def update_status(state):
    if state == "listening":
        status_canvas.itemconfig(status_circle, fill="#00D2FF")
        chat_label.config(text="Friday is listening...")
    elif state == "speaking":
        status_canvas.itemconfig(status_circle, fill="#10B981" )
        chat_label.config(text="Friday is speaking...")
    elif state == "thinking":
        status_canvas.itemconfig(status_circle, fill="#F59E0B")
        chat_label.config(text="Friday is thinking...")
    else:
        status_canvas.itemconfig(status_circle, fill="#4A5568")
        chat_label.config(text="Friday is waiting")

#Control Functions
is_continuous = False

def stop_audio():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        update_status("idle")
    except Exception as e:
        print("Stop Audio Error:", e)

def continuous_listening():
    global is_continuous
    recognizer = sr.Recognizer()
    while is_continuous:
        try:
            with sr.Microphone() as source:
                window.after(0, lambda: update_status("listening"))
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

                window.after(0, lambda: update_status("thinking"))
                text = recognizer.recognize_google(audio)

                window.after(0, lambda t=text: chat_history.insert(tk.END, f"You:{t}\n"))
                response = check_web_commands(text)

                if response:
                    window.after(0, lambda r=response: chat_history.insert(tk.END, f"Friday: {r}\n"))
                    window.after(0, lambda: update_status("speaking"))
                    speak(response)
        except Exception:
            continue
        window.after(0, lambda: update_status("idle"))

def toggle_mic():
    global is_continuous
    is_continuous = not is_continuous
    if is_continuous:
        mic_button.config(text="Continuous: ON" , bg="#10B981")
        import threading
        threading.Thread(target=continuous_listening, daemon=True).start()
    else:
        mic_button.config(text=" continuous: OFF", bg="#374151")
        update_status("idle")




#Control Button
control_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
control_frame.pack(pady=5)

mic_button = tk.Button(
    control_frame,
    text="Continous: OFF",
    font=("Segoe UI", 9, "bold"),
    bg="#374151",
    fg="#FFFFFF",
    relief="flat",
    command=toggle_mic
)
mic_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(
    control_frame,
    text="stop Audio",
    font=("Segoe UI", 9, "bold"),
    bg="#EF4444",
    fg="#FFFFFF",
    command=stop_audio
)
stop_button.pack(side=tk.LEFT, padx=5)



#Main Flow 
name = memory.get("name", "User")
age = memory.get("age", "N/A")
city = memory.get("city", "N/A")
hobby = memory.get("hobby", "N/A")

show_user_info(name, age, city, hobby)
greeting(name)

threading.Thread(target=check_reminders_loop, daemon=True).start()
window.mainloop()