
# This fuction writes required data to a fuctional csv file then copies it as an archive file to OneDrive
# Functional = DO NOT VIEW WHEN RUNNING, will disrupt code routine, in PC directory 
# Archive = Viewable version, will not disrupt code routine, in OneDrive directory

import csv, datetime, os, shutil
from datetime import date

file_list = str                 # Lists all file names in src_folder
num_files = int                 # Number of files in src_folder
header = list                   # Data labels for csv file
today = date.today()            # Today's date, required data parameter
now = datetime.datetime.now()   # Current time, used in variable hr
hr = now.hour                   # Current hr, used with spec_sched as required data parameter
file = ''                       # Full address of file to be transferred 

# Folder containing files to be transferred
src_folder = 'C:\\Python\\directory\\csv\\'
# Folder to recieve files
dst_fodler = 'C:\\Users\\danie\\OneDrive - East Carolina University\\Documents\\data-folder1'

def csv_write(index2, spec_sched, index, cycle_cnt):

    file_list = os.listdir(src_folder)
    num_files = len(file_list)

    ## Creates functional file with data labels if csv file not already created
    if num_files == 0:
        header = ['Date', 'Time', 'Cell']
        # Opens the file in write mode
        with open(f'C:\Python\directory\csv\GUC_Raw{index2}.csv', 'w') as f:
            # Creates the csv writer
            writer = csv.writer(f)
            # Writes header to the csv file
            writer.writerow(header)
        # Update variable values 
        file_list = os.listdir(src_folder)
        num_files = len(file_list)

    ## Writes data to functional file
    # Data to be included in functional file
    data = [f'{today}', f'{hr}:{spec_sched[index]}', f'{cycle_cnt}']
    # Opens the file in the append mode
    with open(f'C:\Python\directory\csv\GUC_Raw{index2}.csv', 'a', newline= "") as f:
        # Creates the csv writer
        writer = csv.writer(f)
        # Writes new row to the csv file
        writer.writerow(data)

    ## Updates archive file
    file = file_list[num_files - 1]
    # Does not copy new archive file if old archive file is open
    try:
        shutil.copy(src_folder + file, dst_fodler)                                       
    except IOError:
        pass
        