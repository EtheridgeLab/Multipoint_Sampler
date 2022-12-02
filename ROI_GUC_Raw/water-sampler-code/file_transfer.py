
# This function transfers old files from the src_folder to the dst_folder
# Original code from https://www.youtube.com/watch?v=CnRMQnmrQ2Y 

import os, shutil
      
file_list = str         # Lists all file names in src_folder
num_files = int         # Number of files in src_folder
file = ''               # Full address of file to be transferred 

# Folder containing files to be transferred
src_folder = 'C:\\Python\\directory\\anapro\\'
# Folder to recieve files
dst_fodler = 'C:\\Users\\danie\\OneDrive - East Carolina University\\Documents\\data-folder1'

def file_transfer(): 

    # Lists names and gets number of files in src_folder
    file_list = os.listdir(src_folder)
    num_files = len(file_list)
    n = num_files - 2

    # Moves old files after new anapro files are added to folder
    while n > 0:
        file = file_list[num_files - 1]
        shutil.move(src_folder + file, dst_fodler)
        n -= 1
        return 1
    