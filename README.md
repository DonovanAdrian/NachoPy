# NachoPy
> made by Donovan Adrian in Python

## Welcome!
 This script is meant to *assist* in the recovery of USER files from a 
 deteriorating drive. To emphasize, this doesn't do anything fancy. The 
 script assumes that the source drive is functional and relevant user files 
 are intact when transferred to a separate drive. Now then! When I found 
 myself with some of my older computer's aging drives going the way of 
 the dodo... I decided to create a script to help ensure that my precious 
 files wouldn't be lost forever. In addition to utilizing cloud backup 
 programs, I wanted an extra layer of assurance! ...And an excuse for 
 some extra practice with Python, of course. Mostly the latter.

## What's The Difference Between v1.0 and v1.1?
 Version 1.0 achieves the core goal; basic file copy of all of the files 
 within the user-defined source drive. Nothing fancy there. v1.0 is a 
 great option if you always want to have anything and everything as far 
 as user directories go, this includes any accessible hidden system files.
 
 Version 1.1 on the other hand offers more user customization for a
 granular copy of the data. You can narrow down what file types you
 don't want, what users you want to ignore, and more. The v1.1 
 downloadable has some examples of what you could ignore already 
 filled in. v1.1 is a great option for a much cleaner copy without 
 any messy hidden files like v1.0. For more info, see the section below
 regarding fine-tuning your copy.

## What Are Some Possible Use Cases For This Script?
 At this time I am only supporting Windows "recovery", grabbing core 
 files that most basic users would find necessary. This includes 
 documents, pictures, music, and downloads that may exist in the expected
 locations. **As a result**, installed programs that may exist on a given 
 drive are not intended to be transferred with this script.

## Do You Have Any Other Plans For This Script?
 At some point I would like to include Unix support in order to broaden 
 the use case as well as this script's potential. Ideally, I'd like for
 this detection to be automatic.

## (Version 1.1) What Are Some Ways I Can Fine-Tune My Copy?
 First, open nacho.py in a text editor. The following variables are
 available and are intended to be updated by the user.
- debug 
  - Options: True or False
  - Info: Enabling debug will show more verbose details. Every single 
 copied, missed, skipped, or ignored file will be output into the console.
- ignoredFileTypes
  - Options: [] or ['.x'] or ['.x', '.y'] etc
  - Info: Specific file types that need to be ignored can be entered 
 within the brackets with ' ' quotations.
  - NOTE: Please use the format '.xyz'
- ignoredFiles
  - Options: [] or ['x.x'] or ['x.x', 'y.y'] etc
  - Info: Specific files that need to be ignored can be entered within
 the brackets with ' ' quotations.
- ignoredUsers
  - Options: [] or ['x'] or ['x', 'y'] etc
  - Info: Specific user directories that need to be ignored can be 
 entered within the brackets with ' ' quotations.

---------------------------------------------------

---------------------------------------------------

---------------------------------------------------

## Planned Script Workflow
- Run Script From Command Line
  - Check If Running On Compatible OS
  - Scan For Connected Drives And Output Results
    - If more than one drive is connected, continue
  - ***Ask User For Desired Source Drive*** *(Integer)*
  - Check Source Drive Compatibility
    - If expected files exist, continue
  - ***Ask User For Desired Destination Drive*** *(Integer)*
  - Copy Files To Root Directory Of Destination Drive
- Complete!
