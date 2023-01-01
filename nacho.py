'''
 * This project was created by Donovan Adrian and any
 * edits or changes must be confirmed as valid by Donovan
 * with written consent under any circumstance.
 *
 * nacho.py Version 1.0
'''

from distutils.dir_util import copy_tree
import platform
import shutil
import time
import sys
import os

# User Updatable Variable
debug = False
ignoredFileTypes = []
ignoredFiles = ['desktop.ini', 'ntuser.dat', 'ntuser.ini']

connectedDrives = []
sourceDrive = ''
destinationDrive = ''
copiedDireCount = 0
copiedFileCount = 0
missedDireCount = 0
missedFileCount = 0
ignoredFileCount = 0


def clean_exit(message):
    print('\n' + message)
    input('\nPress "Enter" to continue...')
    print('\nExiting...\n')
    sys.exit()


def welcome_message():
    print('\n\n'
          '*****************************\n'
          'Welcome to the NachoPy Script\n'
          '         Version 1.1a        \n'
          '*****************************\n')


def check_drives():
    global connectedDrives
    drives = [chr(x) + ':' for x in range(65, 91) if os.path.exists(chr(x) + ':')]
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
        clean_exit('Error: The source drive did not contain the expected user files. Please try again! Exiting...')


def prep_destination_drive():
    global connectedDrives
    global destinationDrive
    check_destination_dir = os.path.isdir(connectedDrives[destinationDrive] + '\\NachoPyDrop')
    if not check_destination_dir:
        print('\nCreating New Directory For Destination Drive...')
        path = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
        os.mkdir(path)


def select_drive(drive_string):
    global connectedDrives
    global destinationDrive
    global sourceDrive
    print('\n\nPlease select a ' + drive_string + ' drive from 0 to ' + str(len(connectedDrives) - 1))
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


def check_ignored_files(file):
    global ignoredFiles
    global ignoredFileTypes
    ignore_file_bool = False
    for ignoredType in ignoredFileTypes:
        if ignoredType in file:
            ignore_file_bool = True
            break
    if file not in ignoredFiles and not ignore_file_bool:
        return False
    return True


def collect_parent_dirs():
    global ignoredFileCount
    global connectedDrives
    global destinationDrive
    global sourceDrive
    source_dir = os.path.join(connectedDrives[sourceDrive], '\\Users')
    dest_dir = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
    for file in os.listdir(source_dir):
        if not check_ignored_files(file):
            child_item = os.path.join(source_dir, file)
            copy_files(child_item, dest_dir)
        elif debug:
            print(file + ' ignored...')
            ignoredFileCount += 1
        else:
            ignoredFileCount += 1


def copy_files(src, dst):
    global ignoredFileCount
    global copiedDireCount
    global copiedFileCount
    global missedDireCount
    global missedFileCount
    global debug
    if not debug:
        print('Copying ' + src + '...', end="", flush=True)
    else:
        print('Copying ' + src + '...')
    dst = os.path.join(dst, os.path.basename(src))
    try:
        for item in os.listdir(src):
            if not check_ignored_files(item):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if debug:
                    print('Copying ' + s + ' to ' + d)
                if os.path.isdir(s):
                    try:
                        copy_tree(s, d)
                        copiedDireCount += 1
                        if not debug:
                            print('.', end="", flush=True)
                    except:
                        if debug:
                            print('Error: Could not copy directory ' + item + '!')
                        missedDireCount += 1
                else:
                    try:
                        shutil.copy2(s, d)
                        copiedFileCount += 1
                        if not debug:
                            print('.', end="", flush=True)
                    except:
                        if debug:
                            print('Error: Could not copy file ' + item + '!')
                        missedFileCount += 1
            elif debug:
                print(item + ' ignored...')
                ignoredFileCount += 1
            else:
                ignoredFileCount += 1
    except:
        pass
    print('\n')


def main():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    global ignoredFileCount
    global copiedFileCount
    global missedFileCount
    if platform.system() != 'Windows':
        clean_exit('Please only use this script in Windows!')
    print('Checking Connected Drives...')
    check_drives()
    select_drive('source')
    print('Source drive check complete!')
    if len(connectedDrives) == 2:
        destinationDrive = 1 - sourceDrive
        print('\n\nDrive ' + connectedDrives[destinationDrive] + ' automatically selected!')
        prep_destination_drive()
    else:
        select_drive('destination')
    print('Destination drive ready!')
    print('\n\n\nSelected Settings:\nSource Location: ' + connectedDrives[sourceDrive] +
          '\\Users\\*\nDestination Location: ' + connectedDrives[destinationDrive] + '\\NachoPyDrop')
    input('\nReady for transfer! Press "Enter" to continue or press "Ctrl + C" to cancel...')
    start_time = time.time()
    print('\n\nCollecting Files... Please Wait...\n\n')
    collect_parent_dirs()
    end_time = time.time()
    completion_time = end_time - start_time
    print('Nacho Run Summary:')
    if completion_time > 60:
        print(' Runtime (HH:MM:SS): ' + time.strftime('%H:%M:%S', time.gmtime(completion_time)))
    else:
        print(' Runtime (Seconds): ' + completion_time)
    print(' Copied Files: ' + str(copiedFileCount))
    print(' Copied Directories: ' + str(copiedDireCount))
    if missedDireCount > 0 or missedFileCount > 0:
        print(' Missed Files: ' + str(missedFileCount))
        print(' Missed Directories: ' + str(missedDireCount))
    if ignoredFileCount > 0:
        print(' Ignored Files: ' + str(ignoredFileCount))
    if missedDireCount > 0 or missedFileCount > 0:
        if debug:
            print('\nSee Above Log For What Files/Directories Were Missed.')
        else:
            print('\nEnable Debugging In The Script To See Which Files/Directories Were Missed.')
    if ignoredFileCount > 0:
        if debug:
            print('\nSee Above Log For What Files/Directories Were Ignored.')
        else:
            print('\nEnable Debugging In The Script To See Which Files/Directories Were Ignored.')
    clean_exit('\nScript complete!')


welcome_message()
main()

