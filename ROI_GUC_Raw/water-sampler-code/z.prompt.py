
# Imports needed directories to execute functions
import time
from threading import local
from set_time_prompt import *
from dae_RelayBoard import *

# Sets comport to correct port used on computer, initializes relay board, sets virtual COM port
COMPORT = "COM3"        
dr = dae_RelayBoard.DAE_RelayBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_16)
dr.initialise(COMPORT)  
dr.setAllStatesOff()

valveMax = ""       # The number of valves to be used for a testing cycle; limits loop to include only used valves
count1 = 0          # Compared to number of valves to be used to collect tubing lengths for each
count2 = 1          # Tracks number of pump/purge cycles. Used to determine which valve is open per cycle  
prepTimes = {}      # Dictionary variable; creates prep_time(valveNumber) variables that extract priming times from function set_time1
time_prep = ""      # Represents water line prime/purge time duration based on cycle count
cycleTime = 0 #1 s  # Duration of time to run pump during scan
timeBalance = ""    # Used to increase duration of cycleTime - adds difference of 250 seconds and prepTime
forward = 15        # Assigns relay to run pump forward/prime
reverse = 16        # Assigns relay to run pump in reverse/purge
# scan = ?          # Input signal from s::can computer
inputMode = 0       # Stores input state from s::can computer. 0 is "off", 1 is "on"

# Designates valves to coresponding relay
valve1 = 1; valve2 = 2; valve3 = 3; valve4 = 4; valve5 = 5; valve6 = 6
# Declaration of dictionary variables (not necessary, used for convinience sake)
prep_time1 = ""; prep_time2 = ""; prep_time3 = ""; prep_time4 = ""; prep_time5 = ""; prep_time6 = ""


# User will be prompted to enter the number of inputs to be used. This will serve as the limit for number of
# cycles to be run before returning to the first input. Input is limited to 1-6; inputs less than 1 or greater
# than 6 will prompt a message to re-enter a value within that range.

print("Please enter number of valves used:")

while True:
    valveMax = int(input('> '))
    print()
    if valveMax < 1 or valveMax > 6:
        print("\n   ***Please enter a value between 1 and 6***\n")
    elif valveMax > 1 or valveMax < 6:
        break


# User will be prompted to input the lengths of tubing connected to each input, limited to the maximum number
# of inputs used. These lengths will be used to determine priming duration for each line.
# Requires function set_time_prompt.

while count1 != valveMax:
    valveNumber = count1 + 1
    print(f"What is the length (in ft.) of the water line connected to Valve {valveNumber}?")
    prepTimes['prep_time' + str(valveNumber)] = set_time_prompt()
    count1 += 1
    locals().update(prepTimes)

time.sleep(1)
print("Beginning new data collection cycle.\n")


# Sets up variable "valve" to be used in place of individual valves
# Allows single routine to control operation of all valves
# Repeats and resets routine if count2 exceeds number of usable valves

while True: 

    if count2 == 1:
        valve = valve1
        time_prep = prep_time1
    elif count2 == 2:
        valve = valve2
        time_prep = prep_time2
    elif count2 == 3:
        valve = valve3
        time_prep = prep_time3
    elif count2 == 4:
        valve = valve4
        time_prep = prep_time4
    elif count2 == 5:
        valve = valve5
        time_prep = prep_time5
    elif count2 == 6:
        valve = valve6
        time_prep = prep_time6
    timeBalance = 250 - time_prep

    # Displays how many input lines are connected, which input line is currently in use, how long the pump will run, 
    # and the delay between pump shut-off and spectrometer scan
    print(f"Number of valves used: {valveMax}")
    print(f"Valve in use: {count2}")
    print(f"Prime duration: {time_prep} seconds")
    print(f"Time offset is: {timeBalance} seconds")

    print("\nWaiting for signal...\n")


    # Program will wait until s::can signal detected
    # Saves 0 or 1 to variable 'inputMode'
    # Requires function scanInput
    inputMode = 1

    # *****Functional routine*****
    # Valves closed on False, open on True

    # When the trigger signal is detected (scanInput returns 1)
    if inputMode == 1:
    # Valve opens, 0.5-second delay, pump engages forward
        dr.setState(valve, True)  
        print(f"Valve {count2} is open.\n")
        time.sleep(0.5)
        print("Priming...\n")
        dr.setState(forward, True) # engages pump
        time.sleep(time_prep)

        # Begin test cycle: valve stays open, pump stops for testing
        print("Testing...\n")
        dr.setState(forward, False) # disengages pump
        dr.setState(valve, False) 
        time.sleep(cycleTime + timeBalance)

        # Purge open valve
        print("Purging...\n")
        dr.setState(valve, True) 
        time.sleep(0.5)
        dr.setState(reverse, True)  # engages pump in reverse
        time.sleep(15)              # 15 seconds
        dr.setState(reverse, False) # disengages pump
        time.sleep(0.5)

        # Closes valve
        dr.setState(valve, False) 
        print(f"Valve {count2} is closed. \n ")

        # When cycle is complete: reset inputMode, increase count2, return to first valve after last valve has been used
        inputMode = 0
        count2 = count2 + 1
        if count2 > valveMax:
            count2 = 1
