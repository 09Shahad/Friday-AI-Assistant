#Friday v0.9
#Developer : Shahad
#Day 9

from cProfile import label
import random
import datetime
import webbrowser
import tkinter as tk

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
    num1 = int(input("First number: "))
    num2 = int(input("Second number: "))
    print("Answer: ", num1 + num2)

def joke():
    print("Why did the computer go to the doctor? Because it caught a virus!")

def show_time():
    now = datetime.datetime.now()
    print("Current time:", now.strftime("%H:%M:%S"))

def show_date():
    now = datetime.datetime.now()
    print("Today's date:", now.strftime("%d/%m/%Y"))

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

name, age, city, hobby = get_user_info()
def show_user_info(name, age, city, hobby):
    print("\n==== Your Information ====")
    print("Name:", name)
    print("Age:", age)
    print("City:", city)
    print("Hobby:", hobby)
    
show_user_info(name, age, city, hobby)

def greeting(name):
    messages = [
        "Hello, " + name + "!",
        "Welcome back, " + name + "!",
        "Nice to see you again, " + name + "!",
        "Good to have you here, " + name + "!"
    ]
    print(random.choice(messages))

#Start of the program
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
print("9. Exit")

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
elif choice == "9":
    print("Goodbye!")
else:
    print("I don't understand.")


window = tk.Tk()
window.title("Friday v0.9")
window.geometry("500x400")
Label = tk.Label(
    window,
    text="Hello, I am Friday.",
    font=("Arial", 16),
)
Label.pack(pady=20)

google_button = tk.Button(
    window,
    text="Open Google",
    command=open_google,
)
google_button.pack(pady=10)

window.mainloop()