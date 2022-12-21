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
    print('\n\n******************************\nWelcome to the NachoPy Script!\n******************************\n')


def check_drives():
    global connectedDrives
    drives = [chr(x) + ':' for x in range(65, 91) if os.path.exists(chr(x) + ':')]
    print(drives)
    drive_num = 0
    for drive in drives:
        print(str(drive_num) + ' -> ' + drive)
        drive_num += 1
        connectedDrives.append(drive)

    if drive_num <= 1:
        clean_exit('\nError: Not enough drives are connected! Please connect at least two drives to the system!')


def pre_screen_drive():
    global connectedDrives
    global sourceDrive
    print('\n\nChecking Source Drive For Valid Files...')
    check_user_dir = os.path.isdir(connectedDrives[sourceDrive] + '\\Users')
    if not check_user_dir:
        clean_exit('\nError: The source drive did not contain the expected user files. Please try again! Exiting...')


def prep_destination_drive():
    global connectedDrives
    global destinationDrive
    check_destination_dir = os.path.isdir(connectedDrives[destinationDrive] + '\\NachoPyDrop')
    if not check_destination_dir:
        print('\n\nCreating New Directory For Destination Drive...')
        path = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
        os.mkdir(path)


def select_drive(drive_string):
    global connectedDrives
    global destinationDrive
    global sourceDrive
    print('\n\nPlease select a ' + drive_string + ' drive from 0 to ' + str(len(connectedDrives)))
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
            print('Please only enter a ' + str(input_type) + '! Try again...\n')
            pass


def collect_files():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    source_dir = os.path.join(connectedDrives[sourceDrive], '\\Users')
    dest_dir = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
    for file in os.listdir(source_dir):
        copy(file, dest_dir)


def copy(src, dst):
    print('\nCopying ' + src + '...')
    try:
        shutil.copy(src, dst)
    except shutil.SameFileError:
        print('\nError: The source and destination are the same!')
    except PermissionError:
        print('\nError: Permission denied! Try running this script as administrator!')
    except:
        print('\nError: Could not copy this file!')


def main():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    if platform.system() != 'Windows':
        clean_exit('Please only use this script in Windows!')
    print('Checking Connected Drives...')
    check_drives()
    select_drive('source')
    if len(connectedDrives) == 2:
        destinationDrive = 1 - sourceDrive
        prep_destination_drive()
    else:
        select_drive('destination')
    print('\n\nCollecting Files... Please Wait...')
    collect_files()
    clean_exit('\nScript complete!')


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
