#Friday v1.0
#Developer : Shahad
#Day 10/11/12


#import
import random
import datetime
import webbrowser
import tkinter as tk

#Memory
memory={}

secret_number = random.randint(1,10)

#Functions
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


def calculator():
    num1 = int(number1.get())
    num2 = int(number2.get())
    answer = num1 + num2
    result_label.config(text="Answer: " + str(answer))


def joke():
    jokes=[
        "Why did the computer go to the doctor? Becuase it caught a viruse!",
        "Why do pragrammers loves python? Becuase it's easy to read!",
        "Why was the computer cold? It forget to close windows!",
        "Debugging: Being the detective in a crime movie where you're also the criminal."
    ]
    result_label.config(text=random.choice(jokes))


def chat():
    message = str(chat_entry.get()).strip().lower()
    print("Message =", repr(message))
    chat_history.insert(tk.END, "You: " + message + "\n")

    if message == "hi":
        result_label.config(text="Hello!")
        chat_history.insert(tk.END, "Friday: Hello!\n")

    elif message == "hey":
        result_label.config(text="Hey!")
        chat_history.insert(tk.END, "Friday: Hey!\n")

    elif message == "hello":
        result_label.config(text="Welcome back, " + memory["name"] + "!")
        chat_history.insert(
            tk.END,
            "Friday: Welcome back, " + memory["name"] +"!\n"
        )
    elif message == "how are you":
        result_label.config(text="I'm doing great! ")
        chat_history.insert(
            tk.END,
            "Friday: I'm doing great!\n"
        )
    elif message == "what's your name?":
        result_label.config(text="My name is Friday!")
        chat_history.insert(tk.END, "Friday:My name is Friday!\n")
    
    elif  message == "who are you":
        result_label.config(text="I'm Friday, an AI assistant!")
        chat_history.insert(tk.END, "Friday:I'm Friday, an AI assistant!\n")
    
    elif message == "how old are you":
        result_label.config(text="I'm still growing and learning!")
        chat_history.insert(tk.END, "Friday:I'm still growing and learning!\n")

    elif message == "bye":
        result_label.config(text="Goodbye!")
        chat_history.insert(
            tk.END,
            "Friday: Goodbye!\n"
        )
    else:
        result_label.config(text="I don't understand.")
        chat_history.insert(
            tk.END,
            "Friday: I don't understand.\n"
        )
    chat_entry.delete(0, tk.END)


def show_time():
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    result_label.config(text="Current Time: " + time)


def show_date():
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    result_label.config(text="Current Date: " + date)

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


#Window
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
name, age, city, hobby = get_user_info()
memory["name"] = name
memory["age"] = age
memory["city"] = city
memory["hobby"] = hobby

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