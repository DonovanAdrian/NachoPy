import platform
import shutil
import sys
import os

connectedDrives = []
sourceDrive = ''
destinationDrive = ''


def clean_exit(message):
    print('\n' + message)
    input('\nPress any key to continue...')
    print('\nExiting...\n')
    sys.exit()


def welcome_message():
    print('\n******************************\nWelcome to the NachoPy Script!\n******************************\n')


def check_drives():
    drives = [chr(x) + ':' for x in range(65, 91) if os.path.exists(chr(x) + ':')]
    print(drives)
    print(type(drives))
    # Loop through connected drives (print out #-n) and ask user which drive to select for A, source, and B, destination
    # When checking source drive, pre-screen drive and look for valid files
    print('Save the above drives to connectedDrives')
    # If there are no drives found... Exit? I guess?


def pre_screen_drive():
    print('This will check the source drive, ' + sourceDrive)


def select_drive(drive_string):
    global destinationDrive
    global sourceDrive
    print('Please select a ' + drive_string + ' drive')
    print(drive_string)
    if drive_string == "destination":
        destinationDrive = _input('', int)
    elif drive_string == "source":
        sourceDrive = _input('', int)
        pre_screen_drive()


def _input(message, input_type=str):
    while True:
        try:
            return input_type (input(message))
        except:pass


def collect_files():
    print('This doesn\'t do anything yet!')
    # Look in the selected drive for /user/ files. Collect all files within and copy to desired drive using copy()
    # I don't remember if shutil does directories AND files?


def copy(src, dst):
    try:
        shutil.copy(src, dst)
    except shutil.SameFileError:
        print('Error: The source and destination are the same!')
    except PermissionError:
        print('Error: Permission denied!')
    except:
        print('Error: Could not copy this file!')


def main():
    if platform.system() != 'Windows':
        clean_exit('Please only use this script in Windows!')
    
    print('Checking Connected Drives...')
    check_drives()
    # print('Checking For Valid Files...')
    # collect_files()
    clean_exit('Script complete!')


welcome_message()
main()


'''
Other stuff
out = os.path.isdir('C:\\Users')
out = os.path.isfile('C:\\Users\foo.csv')
cwd = os.getcwd()
path = os.path.join(parent_dir, directory)
os.mkdir(path)
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        print(d)
my_list = ['blah', 'foo', 'bar']
if item in my_list:
    # whatever

Just in case
https://www.geeksforgeeks.org/implementation-of-dynamic-array-in-python/
'''
