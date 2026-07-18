#Friday v0.7
#Developer : Shahad
#Day 7

import random

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
print("4. Exit")

choice = input("Choose a number: ")
if choice == "1":
    talk(name, hobby, age)
elif choice == "2":
    calculator()
elif choice == "3":
    joke()
elif choice == "4":
    print("Goodbye!")
else:
    print("I don't understand.")