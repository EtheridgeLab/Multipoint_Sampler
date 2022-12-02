
# Code description

# The number of valves to be used. Limits job to include only used valves
# Enter number of valves to be used:
valve_max = 7

# Length of tubing used for each sampling point. Allows for variable priming times based on tubing lengths
# Enter length of line attached to Valve 1:
length1 = 10
# Enter length of line attached to Valve 2:
length2 = 10
# Enter length of line attached to Valve 3:
length3 = 30
# Enter length of line attached to Valve 4:
length4 = 30
# Enter length of line attached to Valve 5:
length5 = 50
# Enter length of line attached to Valve 6:
length6 = 50
# Enter length of line attached to Valve 7: 
length7 = 70

# Time for first sample to be taken ['HH', 'MM']
# Enter time for first sample to be collected:
usr_st_time = ['14', '43']      

# Timing interval. Minutes in between samples
# Enter the interval at which samples are to be collected:
interval = 2

# *****************ENSURE THAT THE SPECTROMETER DELAY IS SET TO THE SAME TIMING INTERVAL**********************************


import time, schedule, datetime, math
from set_time_auto import *
from dae_RelayBoard import *
from file_transfer import *
from csv_write import *

# Sets comport to correct port, initializes relay board, sets virtual COM port
COMPORT = "COM3"        
#dr = dae_RelayBoard.DAE_RelayBoard(dae_RelayBoard.DAE_RELAYBOARD_TYPE_16)
#dr.initialise(COMPORT)
#dr.setAllStatesOff()

cycle_cnt = 1           # Tracks number of pump/purge cycles. Used to determine which valve is open per cycle   
indicator = int         # Indicates when job has been run. 1 when run. Resets after job gets schedule
valve = int             # Represents specific valves based on cycle_cnt
prime_time = int        # Represents water line prime/purge time duration based on cycle_cnt
time_blnce = int        # Timing offset. Aligns priming time and spectrometer sampling time
spec_dur = 10           # Duration of time (sec) it takes for spectrometer to sample
forward = 8             # Assigns relay to run pump forward/prime
reverse = 7             # Assigns relay to run pump in reverse/purge
today = ''              # Current date
now = ''                # Current date and time
index2 = 1              # Index for csv file
usr_hr = int            # Hour value of usr_st_time 
adj_hr = int            # Adjusted usr_hr value. Used to change usr_st_time hour format from string to datetime.time
usr_min = int           # Minute value of usr_st_time
adj_min = int           # Adjusted usr_min value. Used to change usr_st_time minute format from string to datetime.time
adj_st_time = ''        # Adjusted usr_st_time. Starts first job such that first sample is collected at usr_st_time
entry_cnt = 0           # Compared against entries. Stops adding minute entries to lists once lists are filled
job_mins = int          # Used with interval to create job_sched. The minutes (MM) at which the a job will execute
job_sched = []          # List of job_mins. Times (MM) for job to be scheduled
spec_mins = ''          # Used with interval to create spec_sched. The minutes (MM) at which the spectrometer will sample
spec_sched = []         # List of spec_mins. Times (MM) for spectrometer to sample
index = 0               # Index for lists. Allows for constant updates to job execution and sample collection time
hr = ''                 # Current hour
min = ''                # Current minute
time_dif = ''           # Difference in time (min) between usr_min and min. Used to check for errors
gen_st = ''             # Soonest time a sample can be collected. Shown to usr if error executes
cycle_dur = ''          # Estimated total amount of time it takes to complete a job 
dig_break = 0           # Breaks all code loops if 1. Result of error
job_time = ''           # Time (HH:MM) at which job will be scheduled to execute

# Designates valves to coresponding relay
valve1 = 16; valve2 = 4; valve3 = 3; valve4 = 4; valve5 = 5; valve6 = 6; valve7 = 7

# List of lengths. Used to find max length in adv_st
lengths = [length1, length2, length3, length4, length5, length6, length7]

# Number of minutes needed to prime in advance to usr_st_time
adv_st = math.ceil(set_time_auto(max(lengths)) / 60)

# Number of times to be created in job_sched
entries = math.floor(60 / interval)     


# Job to be executed by scheduler
def job():

    global index2
    global cycle_cnt
    global indicator

    # Sets up variable "valve" to be used in place of individual valves. Allows single routine to control 
    # operation of all valves. Repeats and resets routine if cycle_cnt exceeds number of usable valves
    # Uses function set_time_auto to assign prime time based on length of tubing
    if cycle_cnt == 1:
        valve = valve1
        prime_time = set_time_auto(length1)
    elif cycle_cnt == 2:
        valve = valve2
        prime_time = set_time_auto(length2)
    elif cycle_cnt == 3:
        valve = valve3
        prime_time = set_time_auto(length3)
    elif cycle_cnt == 4:
        valve = valve4
        prime_time = set_time_auto(length4)
    elif cycle_cnt == 5:
        valve = valve5
        prime_time = set_time_auto(length5)
    elif cycle_cnt == 6:
        valve = valve6
        prime_time = set_time_auto(length6)
    elif cycle_cnt == 7:
        valve = valve7
        prime_time = set_time_auto(length7)

    # Aligns timing with anapro software
    time_blnce = (adv_st * 60) - prime_time - 2 
    time.sleep(time_blnce)
    
    # Displays how many input lines are connected, which input line is currently in use, and how long the pump will run
    print(f"\nNumber of valves used: {valve_max}")
    print(f"Valve in use: {cycle_cnt}")
    print(f"Prime duration: {prime_time} seconds\n")

    # *****Functional routine*****
    # Valves closed on False, open on True

    # Valve opens, 1-second delay, pump engages forward
    #dr.setState(valve, True)
    print(f"Valve {cycle_cnt} is open.\n")
    time.sleep(1)
    print("Priming...")
    #dr.setState(forward, True) # engages pump
    time.sleep(prime_time)

    # Begin test cycle: valve closes, pump stops for testing
    #dr.setState(forward, False) # disengages pump
    time.sleep(1)
    #dr.setState(valve, False) 
    print("Testing...")
    time.sleep(spec_dur)

    # Purge open valve
    print("Purging...\n")
    #dr.setState(valve, True) 
    time.sleep(1)
    #dr.setState(reverse, True)  # engages pump in reverse
    time.sleep(prime_time)       
    #dr.setState(reverse, False) # disengages pump
    time.sleep(1)

    # Closes valve
    #dr.setState(valve, False) 
    print(f"Valve {cycle_cnt} is closed. \n ")    

    # *****File transfer routine*****

    # Uses function file_transfer to transfer all files in folder if files created by anapro
    file_transfer()
    csv_write(index2, spec_sched, index, cycle_cnt)
    x = file_transfer()
    if x == 1:
        index2 += 1
        x = 0

    # When cycle is complete: increase cycle_cnt, return to first valve after last valve has been used, set indicator to 1
    cycle_cnt += 1
    if cycle_cnt > valve_max:
        cycle_cnt = 1
    indicator = 1


# Advances usr_st_time by adv_st minutes to create adj_st_time. Starts job soon enough to take first sample at usr_st_time
usr_hr = int(usr_st_time[0])
usr_min = int(usr_st_time[1])
if usr_min < adv_st:
    adj_min = 60 + usr_min - adv_st 
    adj_hr = usr_hr - 1
    adj_st_time = datetime.time(adj_hr, adj_min, 00) 
else:
    adj_min = usr_min - adv_st
    adj_st_time = datetime.time(usr_hr, adj_min, 00) 

# Adds entries to job_sched based on adj_st_time and interval
job_mins = adj_st_time.minute
while entry_cnt < entries:
    if job_mins < 10:
        job_sched.append('0' + str(job_mins))
        job_mins += interval
        entry_cnt += 1
        if entry_cnt == entries:
            break
    elif job_mins < 60:
        job_sched.append(str(job_mins))
        job_mins += interval
        entry_cnt += 1
        if entry_cnt == entries:
            break
    elif job_mins >= 60:
        job_mins = job_mins - 60

# Reset entry_cnt
entry_cnt = 0

# Adds entries to spec_sched based on usr_st_time and interval
spec_mins = usr_min
while entry_cnt < entries:
    if spec_mins < 10:
        spec_sched.append('0' + str(spec_mins))
        spec_mins += interval
        entry_cnt += 1
        if entry_cnt == entries:
            break
    elif spec_mins < 60:
        spec_sched.append(str(spec_mins))
        spec_mins += interval
        entry_cnt += 1
        if entry_cnt == entries:
            break
    elif spec_mins >= 60:
        spec_mins = spec_mins - 60


# Prints user entered information about first sample time and interval
print(f'\nFirst sample scheduled for: {usr_st_time[0]}:{usr_st_time[1]}')
print(f'Samples will be taken every {interval} minutes')

# Checks for errors then executes first job when now passes adj_st_time
# Ensures that first spectrometer sampling will occur at usr_st_time
while True: 
    now = datetime.datetime.now()
    min = now.minute 
    hr = now.hour
    # Creates time_dif
    if usr_min < min:
        time_dif = usr_min + adv_st - min
    else:
        time_dif = usr_min - min
    # Creates gen_st
    if min + adv_st < 10:
        gen_st = str(hr) + ':' + '0' + str(min + adv_st)
    elif min + adv_st > 59:
        if hr == usr_hr:
            gen_st = str(hr) + ':' + str(min + adv_st - 60)
        else:
            gen_st = str(hr + 1) + ':' + str(min + adv_st - 60)
    else:
        gen_st = str(hr) + ':' + str(min + adv_st)
  

    # Error 1. Breaks code if usr_st_time does not allow enough time for longest priming time
    if usr_hr < hr:
        dig_break = 1
        print(f'\nerror: not enough time before {usr_st_time[0]}:{usr_st_time[1]} to prime')
        print(f'> soonest available start time: {gen_st} <\n')
        break
    if usr_hr == hr:
        if time_dif < adv_st:
            dig_break = 1
            print(f'\nerror: not enough time before {usr_st_time[0]}:{usr_st_time[1]} to prime')
            print(f'> soonest available start time: {gen_st} <\n')
            break

    # Error 2. Breaks code if interval is too short for longest priming time
    cycle_dur = adv_st * 2
    if cycle_dur > interval:
        dig_break = 1
        print(f'\nerror: {interval} minute interval too short for some prime durations')
        print(f'> shortest allowable interval: {cycle_dur} <\n')
        break

    if now.time() >= adj_st_time:
        job()
        time.sleep(1)
        indicator = 0
        index += 1
        break

# *****Timing routine*****
# Schedules subsequent jobs to execute at job_time and prints when sample will be taken

while True:
    if dig_break == 1:
        break
    now = datetime.datetime.now()    
    # Structures job_time as "HH:MM"
    hr = str(now.hour)
    if int(hr) < 10:
        hr = '0' + hr
    job_time = hr + ':' + job_sched[index]
    # Enures sample schedule display hour is correct
    hr = str(now.hour)
    if int(spec_sched[index]) < int(job_sched[index]):
        hr = str(int(hr) + 1)
        if int(hr) == 24:
            hr = 0
    if int(hr) < 10:
        hr = '0' + str(hr)
    
    print(f'Next sample scheduled for: {hr}:{spec_sched[index]}')
    schedule.every().day.at(job_time).do(job)

    # Runs pending job
    while True:
        schedule.run_pending()
        time.sleep(1)
        # Breaks loop once job is run
        if indicator == 1:    
            break
    
    # Clears schedule and resets indicator. Adds one to index until it resets
    schedule.clear()    
    indicator = 0
    index += 1
    if index >= entries:
        index = 0 
