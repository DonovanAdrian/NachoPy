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
    global connectedDrives
    drives = [chr(x) + ':' for x in range(65, 91) if os.path.exists(chr(x) + ':')]
    print(drives)
    print(type(drives))
    drive_num = 0
    for drive in drives:
        print(str(drive_num) + ' -> ' + drive)
        drive_num += drive_num
        connectedDrives.append(drive)

    if drive_num <= 1:
        clean_exit('Not enough drives are connected! Please connect at least two drives to the system!')


def pre_screen_drive():
    global connectedDrives
    global sourceDrive
    print('Checking Source Drive For Valid Files...')
    check_user_dir = os.path.isdir(connectedDrives[sourceDrive] + '\\Users')
    if not check_user_dir:
        clean_exit('The source drive did not contain the expected user files. Please try again! Exiting...')


def prep_destination_drive():
    global connectedDrives
    global destinationDrive
    check_destination_dir = os.path.isdir(connectedDrives[destinationDrive], '\\NachoPyDrop')
    if not check_destination_dir:
        print('Creating New Directory For Destination Drive...')
        path = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
        os.mkdir(path)


def select_drive(drive_string):
    global destinationDrive
    global sourceDrive
    global connectedDrives
    print('Please select a ' + drive_string + ' drive')
    print(drive_string)
    if drive_string == "destination":
        destinationDrive = _input('', int)
        prep_destination_drive()
    elif drive_string == "source":
        sourceDrive = _input('', int)
        pre_screen_drive()


def _input(message, input_type=str):
    while True:
        try:
            return input_type (input(message))
        except:
            clean_exit('You entered an invalid value that was not expected! Exiting...')


def collect_files():
    print('This doesn\'t do anything yet!')
    # Look in the selected drive for <source_letter>/Users/ iterate through users. Use copy() to gather files


def copy(src, dst):
    try:
        shutil.copy(src, dst)
    except shutil.SameFileError:
        print('Error: The source and destination are the same!')
    except PermissionError:
        print('Error: Permission denied! Try running this script as administrator!')
    except:
        print('Error: Could not copy this file!')


def main():
    if platform.system() != 'Windows':
        clean_exit('Please only use this script in Windows!')
    
    print('Checking Connected Drives...')
    check_drives()
    select_drive('source')
    select_drive('destination')
    # collect_files()
    clean_exit('Script complete!')


welcome_message()
main()


'''
Other stuff
for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
        print(d)
my_list = ['blah', 'foo', 'bar']
if item in my_list:
    # whatever
'''
