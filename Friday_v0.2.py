#Friday v0.2 -- day 2
print("Hello! I am Friday.")
name = input("What is your name? ")
print("Nice to meet you, " + name + "! How can I assist you today? ")
mood = input("How are you feeling today? ")
if mood == "fine" :
    print("Happy to hear that! ")
elif mood == "good" :
    print("That's great! ") 
elif mood == "sad" :   
    print("I am sorry to hear that.")
elif mood == "tried" :
    print("I hope you get some rest soon.")
else :
    print("Thank you for telling me. ")
print("Goodbye!")
