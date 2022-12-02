
#1 original code, works from python scheduler and uses variables to align timing
# good because it works, bad becuase variables are dictating timing
import datetime, schedule, time

while True:

    # Creates variable time_now in loop so that it's constantly updated to the current time
    time_now = datetime.datetime.now()

    # Starts job when time_now is past start_time, schedules job to repeat every interval, and executes pending jobs
    if time_now.time() >= start_time.time():
        job()
        schedule.every(interval).minutes.at(":00").do(job)
        while True:
            schedule.run_pending()

time_balance = int      # Timing offset. Aligns priming time and spectrometer sampling time
sample_time = 10        # Duration of time (in seconds) for spectrometer to sample
max_cycle_time = 60 #120 #420 # Maximum time (in seconds) needed to execute a job rounded up to nearest minute. Accounts for lack of scheduler awareness of job execution time
cycle_time = int        # Actual time used to execute a job
interval = 1 #3 # 8        # Timing interval. Samples will be taken this many minutes plus max_cycle_time apart

# Time to start first data collection cycle. The date is irrelevant, only need time for job to start
# Should always be scheduled such that priming begins 3 minutes before spectrometer sampling to allow time for water priming
start_time = datetime.datetime(2022, 1, 1, 16, 19, 0, 0)

time_balance = 60 - time_prep - 2

cycle_time = (time_prep * 2) + time_balance + sample_time + 4
time.sleep(max_cycle_time - cycle_time)


#2 Timing based on updating clock and checking against list, favorite

# Variables and functions
import datetime, schedule, time

start_time = 32
interval = 1 
minute = []
count1 = 0
count2 = int

# Sample job
def job():
        print('job executed')
        global count2
        count2 = 1


# Creates list minute
while start_time < 60:
    if start_time < 10:
        minute.append('0' + str(start_time))
        start_time += interval
    else:
        minute.append(str(start_time))
        start_time += interval

# Timing loop
while True: 

    now = datetime.datetime.now()
    hour = str(now.hour)
    sample_time = hour + ':' + minute[count1]
    schedule.every().day.at(sample_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
        if count2 == 1:
            break
    
    count2 = 0
    count1 += 1
    if count1 > 60 / interval:
        count1 = 0 



#3 timing based on comparing minutes to clock
# good bc it works and is based on clock, bad because depends on count, if count misses first go sampling gets messed up


import datetime, time

count = 0 

def job():
    print('job executed')

while True:

    now = datetime.datetime.now()
    minute = str(now.minute)
    second = str(now.second)

    start_time = ['50:0', '51:0', '52:0', '53:0']
    check_time = minute + ':' + second

    if start_time[count] == check_time:
        job()
        count = count + 1
        if count > 3:
            count = 0


# old code for printing sample time

disp_time = int         # Displays what time sample is scheduled to be taken

disp_time = int(job_sched[index]) + adv_st
if disp_time == 60:
    if hr == 23:
        print(f'Next sample scheduled for: 00:00')
    else:
        print(f'Next sample scheduled for: {int(hr) + 1}:00')   
else:
    print(f'Next sample scheduled for: {hr}:{disp_time}')   