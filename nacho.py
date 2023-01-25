'''
 * This project was created by Donovan Adrian and any
 * edits or changes must be confirmed as valid by Donovan
 * with written consent under any circumstance.
 *
 * nacho.py Version 1.1
'''

from shutil import copy2, copystat, Error
from datetime import datetime
import platform
import random
import string
import time
import sys
import os

'''
************************************************
*********** User Updatable Variables ***********
************************************************
'''

debug = False
debugLogOutput = True
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
debugLogCollection = []
sourceDrive = ''
destinationDrive = ''
copiedFileCount = 0
missedFileCount = 0
skippedDirCount = 0
skippedFileCount = 0
ignoredFileCount = 0
ignoredUserCount = 0
dtStringInitiated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def clean_exit(message):
    print('\n' + message)
    input('\nPress "Enter" to continue...')
    print('\nExiting...\n')
    sys.exit()


def welcome_message():
    print('\n\n'
          '*****************************\n'
          'Welcome to the NachoPy Script\n'
          '         Version 1.1         \n'
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
            return input_type(input(message))
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


def check_destination_files(src, dst_files):
    for dst_file in dst_files:
        if dst_file in src:
            return True
    return False


def check_directory(input_directory):
    check_dirs = os.listdir(input_directory)
    if len(check_dirs) == 0:
        return False
    for check_dir in check_dirs:
        child_check_elem = os.path.join(input_directory, check_dir)
        try:
            if os.path.isdir(child_check_elem):
                if check_directory(child_check_elem):
                    return True
            else:
                if not check_ignored_files(child_check_elem):
                    return True
        except:
            pass
    return False


def collect_parent_dirs():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    source_dir = os.path.join(connectedDrives[sourceDrive], '\\Users')
    dest_dir = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
    copy_files(source_dir, dest_dir, 3, False)


def copy_files(src, dst, initial_output, ignore_user_check):
    global debugLogCollection
    global ignoredUserCount
    global ignoredFileCount
    global skippedFileCount
    global skippedDirCount
    global copiedFileCount
    global missedFileCount
    global debug

    initial_output -= 1
    if not check_ignored_users(src) or ignore_user_check:
        try:
            if initial_output == 1:
                if debugLogOutput:
                    debugLogCollection.append('\nCopying ' + src + '...')
                if not debug:
                    print('\nCopying ' + src + '...', end="", flush=True)
                else:
                    print('\nCopying ' + src + '...')
            if not os.path.isdir(dst):
                os.makedirs(dst)

            names = os.listdir(src)
            dst_names = os.listdir(dst)
            for name in names:
                if check_ignored_files(name.lower()):
                    if debugLogOutput:
                        debugLogCollection.append('Ignoring ' + name + '...')
                    if debug:
                        print('Ignoring ' + name + '...')
                    ignoredFileCount += 1
                    continue
                srcname = os.path.join(src, name)
                if name not in dst_names or os.path.isdir(srcname):
                    dstname = os.path.join(dst, name)
                    try:
                        if os.path.isdir(srcname):
                            if check_directory(srcname):
                                if initial_output == 1:
                                    ignore_user_check = True
                                    if not debug:
                                        print('.', end="", flush=True)
                                copy_files(srcname, dstname, initial_output, ignore_user_check)
                            else:
                                if debugLogOutput:
                                    debugLogCollection.append('Skipping ' + name + ' due to emptiness or due to all '
                                                                                   'the contained files being ignored.')
                                if debug:
                                    print('Skipping ' + name + ' due to emptiness or due to all the contained files '
                                                               'being ignored.')
                                skippedDirCount += 1
                            continue
                        else:
                            if debugLogOutput:
                                debugLogCollection.append('Copying ' + srcname + ' to ' + dstname)
                            if debug:
                                print('Copying ' + srcname + ' to ' + dstname)
                            copy2(srcname, dstname)
                            copiedFileCount += 1
                    except (IOError, os.error):
                        if debugLogOutput:
                            debugLogCollection.append('Error: Could not copy file ' + name + '!')
                        if debug:
                            print('Error: Could not copy file ' + name + '!')
                        missedFileCount += 1
                    except Error:
                        if debugLogOutput:
                            debugLogCollection.append('Error: Could not copy file ' + name + '!')
                        if debug:
                            print('Error: Could not copy file ' + name + '!')
                        missedFileCount += 1
                else:
                    if debugLogOutput:
                        debugLogCollection.append('Skipping ' + name + ' since it already exists in the destination...')
                    if debug:
                        print('Skipping ' + name + ' since it already exists in the destination...')
                    skippedFileCount += 1
            try:
                if check_ignored_files(src.lower()):
                    if debugLogOutput:
                        debugLogCollection.append('Ignoring ' + src + '...')
                    if debug:
                        print('Ignoring ' + src + '...')
                    ignoredFileCount += 1
                else:
                    dst_files = os.listdir(dst)
                    if not check_destination_files(src, dst_files) and not os.path.isdir(src):
                        if debugLogOutput:
                            debugLogCollection.append('Copying ' + src + ' to ' + dst)
                        if debug:
                            print('Copying ' + src + ' to ' + dst)
                        copystat(src, dst)
                        copiedFileCount += 1
                    elif not os.path.isdir(src):
                        if debugLogOutput:
                            debugLogCollection.append('Skipping ' + src + ' since it already exists in the destination '
                                                                          'and is not a directory...')
                        if debug:
                            print('Skipping ' + src + ' since it already exists in the destination and is not a '
                                                      'directory...')
                        skippedFileCount += 1
            except WindowsError:
                if debugLogOutput:
                    debugLogCollection.append('Error: Could not copy file ' + src + '!')
                if debug:
                    print('Error: Could not copy file ' + src + '!')
                missedFileCount += 1
                pass
            except OSError:
                if debugLogOutput:
                    debugLogCollection.append('Error: Could not copy file ' + src + '!')
                if debug:
                    print('Error: Could not copy file ' + src + '!')
                missedFileCount += 1
                pass
        except:
            pass
    elif initial_output == 1:
        if debugLogOutput:
            debugLogCollection.append('Ignoring User ' + src + '...')
        if debug:
            print('Ignoring User ' + src + '...')
        else:
            print('\nIgnoring User ' + src + '...', end="", flush=True)
        ignoredUserCount += 1


def generate_random_string(letter_count, num_count):
    letters = ''.join(random.choice(string.ascii_letters) for i in range(letter_count))
    numbers = ''.join(random.choice(string.digits) for i in range(num_count))
    alphanumeric = list(letters + numbers)
    random.shuffle(alphanumeric)
    return ''.join(alphanumeric)


def generate_debug_log(completion_time):
    global debugLogCollection
    global dtStringInitiated
    global connectedDrives
    global destinationDrive
    global sourceDrive
    global ignoredUserCount
    global ignoredFileCount
    global skippedFileCount
    global skippedDirCount
    global copiedFileCount
    global missedFileCount
    if len(debugLogCollection) > 0:
        filename_retry = 0
        nacho_file_name = ''
        dest_dir = os.path.join(connectedDrives[destinationDrive], '\\NachoPyDrop')
        dst_names = os.listdir(dest_dir)
        max_random_gen = 10
        random_letter_count = random.randrange(3, 7)
        while filename_retry < 10:
            nacho_file_name = 'NachoDebugLog_' + generate_random_string(random_letter_count, max_random_gen -
                                                                        random_letter_count) + '.txt'
            if nacho_file_name not in dst_names:
                break
            filename_retry += 1
        if filename_retry < 10:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            nacho_file_path = os.path.join(dest_dir, nacho_file_name)
            try:
                nacho_debug_file = open(nacho_file_path, 'w')
                nacho_debug_file.write('Nacho Run Initiated On: ' + dtStringInitiated)
                nacho_debug_file.write('\nNacho Run Completed On: ' + dt_string)
                nacho_debug_file.write('\n\nSelected Settings:\nSource Location: ' + connectedDrives[sourceDrive] +
                                       '\\Users\\*\nDestination Location: ' + connectedDrives[destinationDrive] +
                                       '\\NachoPyDrop')
                nacho_debug_file.write('\n\n\n*******Debug Data*******')
                for debugLine in debugLogCollection:
                    nacho_debug_file.write('\n' + debugLine)
                nacho_debug_file.write('\n\n\n\nNacho Run Summary:')
                if completion_time > 60:
                    nacho_debug_file.write('\n Runtime (HH:MM:SS) -> ' + time.strftime('%H:%M:%S',
                                                                                     time.gmtime(completion_time)))
                else:
                    completion_time = round(completion_time, 2)
                    nacho_debug_file.write('\n Runtime (Seconds) --> ' + str(completion_time))
                nacho_debug_file.write('\n Copied Files -------> ' + str(copiedFileCount))
                if missedFileCount > 0:
                    nacho_debug_file.write('\n Missed Files -------> ' + str(missedFileCount))
                if skippedDirCount > 0:
                    nacho_debug_file.write('\n Skipped Dirs -------> ' + str(skippedDirCount))
                if skippedFileCount > 0:
                    nacho_debug_file.write('\n Skipped Files ------> ' + str(skippedFileCount))
                if ignoredFileCount > 0:
                    nacho_debug_file.write('\n Ignored Files ------> ' + str(ignoredFileCount))
                if ignoredUserCount > 0:
                    nacho_debug_file.write('\n Ignored Users ------> ' + str(ignoredUserCount))
                nacho_debug_file.close()
                print('Debug Log Finished Generating!\n\n')
            except:
                print('Debug Log Generation Error! A File Was Not Generated.\n\n')
        else:
            print('Debug Log Generation Failed! Are There Any Other Logs In The Destination?\n\n')
    else:
        print('No Debug Log Data Collected! A File Was Not Generated.\n\n')


def main():
    global connectedDrives
    global destinationDrive
    global sourceDrive
    global ignoredUserCount
    global ignoredFileCount
    global skippedFileCount
    global skippedDirCount
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
    if debugLogOutput:
        print('\n\nGenerating Debug Log...')
        generate_debug_log(completion_time)
    print('\n\n\n\nNacho Run Summary:')
    if completion_time > 60:
        print(' Runtime (HH:MM:SS) -> ' + time.strftime('%H:%M:%S', time.gmtime(completion_time)))
    else:
        completion_time = round(completion_time, 2)
        print(' Runtime (Seconds) --> ' + str(completion_time))
    print(' Copied Files -------> ' + str(copiedFileCount))
    if missedFileCount > 0:
        print(' Missed Files -------> ' + str(missedFileCount))
    if skippedDirCount > 0:
        print(' Skipped Dirs -------> ' + str(skippedDirCount))
    if skippedFileCount > 0:
        print(' Skipped Files ------> ' + str(skippedFileCount))
    if ignoredFileCount > 0:
        print(' Ignored Files ------> ' + str(ignoredFileCount))
    if ignoredUserCount > 0:
        print(' Ignored Users ------> ' + str(ignoredUserCount))
    print('\n')
    if missedFileCount > 0 or skippedDirCount > 0 or skippedFileCount > 0 or ignoredFileCount > 0 or \
            ignoredUserCount > 0:
        if debugLogOutput and debug:
            print('See Above Log Or Debug Log Output In Destination For More Details.')
        elif debugLogOutput and not debug:
            print('See Debug Log Output In Destination For More Details.')
        elif not debugLogOutput and debug:
            print('See Above Log For More Details.')
        else:
            print('Enable Debugging Or Debug Log Output In The Script For More Details.')
    clean_exit('\nScript complete!')


welcome_message()
main()
