#Friday v0.4
#Developer : Shahad
#Day 4

def talk():
    mood = input("How are you today? ")
    if mood == "fine":
        print("That's good to hear! ")
    elif mood == "sad":
        print("I'm sorry to hear that. ")
    else:
        print("Thank you for telling me. ")

def calculator():
    num1 = int(input("First number: "))
    num2 = int(input("Second number: "))
    print("Answer: ", num1 + num2)

def joke():
    print("Why did the computer go to the doctor? Because it caught a virus!")

    
print("Hello!, I am Friday.")
name = input("What is your name? ")
print(" Welcome back, " + name)

print("\nWhat do you want to do? ")
print("1. Talk")
print("2. Calculator")
print("3. Joke")
print("4. Exit")

choice = input("Choose a number: ")
if choice == "1":
    talk()
elif choice == "2":
    calculator()
elif choice == "3":
    joke()
elif choice == "4":
    print("Goodbye!")
else:
    print("I don't understand.")