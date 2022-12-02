# This function returns a time duration based on a distance entered by the user.
# If  input distance is less than 0 or greater than 100, the user will be prompted
# with a message to reenter a value that falls within the range.

def set_time_prompt(): 

    while True:
        userInput = int(input('> '))
        print()
        if 0 < userInput <= 25:
            seconds = 80
            break
        elif 25 < userInput <= 50:
            seconds = 140
            break
        elif 50 < userInput <= 75:
            seconds = 200
            break
        elif 75 < userInput <= 100:
            seconds = 250
            break
        elif userInput > 100 or userInput <= 0:
            print("Please enter a distance of 1 - 100 ft: ")

    if seconds != None:
        print(f"Length is {userInput} ft.")
        print(f"Line prime and purge times will be {seconds} secs.\n")
 
    return seconds