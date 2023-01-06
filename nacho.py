'''
 * This project was created by Donovan Adrian and any
 * edits or changes must be confirmed as valid by Donovan
 * with written consent under any circumstance.
 *
 * nacho.py Version 1.0
'''

from shutil import copy2, copystat, Error
import platform
import time
import sys
import os

'''
************************************************
*********** User Updatable Variables ***********
************************************************
'''

debug = False
ignoredFileTypes = []
ignoredFiles = ['desktop.ini', 'ntuser.dat', 'ntuser.ini', 'ntuser.pol']
ignoredUsers = ['All Users', 'Default', 'Public']

'''
************************************************
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*********** User Updatable Variables ***********
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
************************************************
Variable Key:
    debug - 
        Options: True or False
        Info: Enabling debug will show more 
         verbose details. Every single copied,
         missed, skipped, or ignored file will
         be output into the console.
    ignoredFileTypes - 
        Options: [] or ['.x'] or ['.x', '.y'] etc
        Info: Specific file types that need
         to be ignored can be entered within
         the brackets with ' ' quotations.
         NOTE: Please use the format '.xyz'
    ignoredFiles - 
        Options: [] or ['x.x'] or ['x.x', 'y.y'] etc
        Info: Specific files that need to be
         ignored can be entered within the
         brackets with ' ' quotations.
    ignoredUsers - 
        Options: [] or ['x'] or ['x', 'y'] etc
        Info: Specific user directories that
         need to be ignored can be entered 
         within the brackets with ' ' quotations.
************************************************
'''

connectedDrives = []
sourceDrive = ''
destinationDrive = ''
copiedFileCount = 0
missedFileCount = 0
ignoredFileCount = 0
ignoredUserCount = 0


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
    for ignoredType in ignoredFileTypes:
        if ignoredType in file:
            return True
    for ignoredFile in ignoredFiles:
        if ignoredFile in file:
            return True
    return False


def check_ignored_users(user_path):
    global ignoredUsers
    for ignoredUser in ignoredUsers:
        if ignoredUser in user_path:
            return True
    return False


def collect_parent_dirs():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    source_dir = os.path.join(connectedDrives[sourceDrive], '\\Users')
    dest_dir = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
    copy_files(source_dir, dest_dir, 3, False)


def copy_files(src, dst, initial_output, ignore_user_check):
    global ignoredUserCount
    global ignoredFileCount
    global copiedFileCount
    global missedFileCount
    global debug

    initial_output -= 1
    if not check_ignored_users(src) or ignore_user_check:
        try:
            if initial_output == 1:
                if not debug:
                    print('\nCopying ' + src + '...', end="", flush=True)
                else:
                    print('\nCopying ' + src + '...')
            if not os.path.isdir(dst):
                os.makedirs(dst)

            names = os.listdir(src)
            for name in names:
                if check_ignored_files(name.lower()):
                    if debug:
                        print('Ignoring ' + name + '...')
                        ignoredFileCount += 1
                    else:
                        ignoredFileCount += 1
                    continue
                srcname = os.path.join(src, name)
                dstname = os.path.join(dst, name)
                try:
                    if os.path.isdir(srcname):
                        if initial_output == 1:
                            ignore_user_check = True
                            if not debug:
                                print('.', end="", flush=True)
                        copy_files(srcname, dstname, initial_output, ignore_user_check)
                    else:
                        if debug:
                            print('Copying ' + srcname + ' to ' + dstname)
                        copy2(srcname, dstname)
                        copiedFileCount += 1
                except (IOError, os.error):
                    if debug:
                        print('Error: Could not copy file ' + name + '!')
                    missedFileCount += 1
                except Error:
                    if debug:
                        print('Error: Could not copy file ' + name + '!')
                    missedFileCount += 1
            try:
                if check_ignored_files(src.lower()):
                    if debug:
                        print('Ignoring ' + src + '...')
                        ignoredFileCount += 1
                    else:
                        ignoredFileCount += 1
                else:
                    if debug:
                        print('Copying ' + srcname + ' to ' + dstname)
                    copystat(src, dst)
                    copiedFileCount += 1
            except WindowsError:
                if debug:
                    print('Error: Could not copy file ' + src + '!')
                missedFileCount += 1
                pass
            except OSError:
                if debug:
                    print('Error: Could not copy file ' + src + '!')
                missedFileCount += 1
                pass
        except:
            pass
    elif initial_output == 1:
        if debug:
            print('Ignoring User ' + src + '...')
        else:
            print('\nIgnoring User ' + src + '...', end="", flush=True)
        ignoredUserCount += 1


def main():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    global ignoredUserCount
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
    print('\n\nNacho Run Summary:')
    if completion_time > 60:
        print(' Runtime (HH:MM:SS): ' + time.strftime('%H:%M:%S', time.gmtime(completion_time)))
    else:
        completion_time = round(completion_time, 2)
        print(' Runtime (Seconds): ' + str(completion_time))
    print(' Copied Files: ' + str(copiedFileCount))
    if missedFileCount > 0:
        print(' Missed Files: ' + str(missedFileCount))
    if ignoredFileCount > 0:
        print(' Ignored Files: ' + str(ignoredFileCount))
    if ignoredUserCount > 0:
        print(' Ignored Users: ' + str(ignoredUserCount))
    print('\n')
    if missedFileCount > 0:
        if debug:
            print('See Above Log For What Files/Directories Were Missed.')
        else:
            print('Enable Debugging In The Script To See Which Files/Directories Were Missed.')
    if ignoredFileCount > 0:
        if debug:
            print('See Above Log For What Files/Directories Were Ignored.')
        else:
            print('Enable Debugging In The Script To See Which Files/Directories Were Ignored.')
    if ignoredUserCount > 0:
        print('See Above Log For What Users Were Ignored.')
    clean_exit('\nScript complete!')


welcome_message()
main()

