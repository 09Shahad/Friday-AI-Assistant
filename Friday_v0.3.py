print("Hello!, I am Friday.")
name = input("What is your name? ")
print(" Welcome back, " + name)

print("\nWhat do you want to do? ")
print("1. Talk")
print("2. calculator")
print("3. Exit")

choice = input("Choose a number: ")
if choice == "1":
    mood = input("How are you feeling today? ")

    if mood == "good":
        print("That's great to hear!")
    elif mood == "fine":
        print("That's good to hear!")
    elif mood == "sad":
        print("I'm sorry to hear that. I hope your day gets better!")
    else :
        print("Thank you for telling me. ")
elif choice == "2":
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    
    print("Answer: " , num1 + num2)

else :
    print("Goodbye! Have a great day!")