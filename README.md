# NachoPy
> made by Donovan Adrian in Python

## Welcome!
 This script is meant to *assist* in the recovery of user files from a 
 deteriorating drive. To emphasize, this doesn't do anything fancy. The 
 script assumes that the source drive is functional and relevant files 
 are intact when transferred to a separate drive. Now then! When I found 
 myself with some of my older computer's aging drives going the way of 
 the dodo... I decided to create a script to help ensure that my files 
 wouldn't be lost forever. In addition to utilizing cloud backup programs, 
 I wanted an extra layer of assurance! ...And an excuse for some extra 
 practice with Python, of course.

## How Well Does This Work?
 Well, it doesn't work quite yet! So far it's just a concept, but I hope
 to finish basic functionality swiftly. I also figured it may be 
 interesting to provide my thought process from beginning to end, just 
 as I have mostly done with some of my other repositories.

## What Are Some Possible Use Cases For This Script?
 At this time I am only supporting Windows recovery assistance, grabbing
 core files that most basic users would find necessary. This includes
 documents, pictures, music, and downloads that may exist in the expected
 locations. As a result, installed programs that may exist on a drive are 
 not intended to be transferred.

## Do You Have Any Other Plans For This Script?
 At this time, I want to complete basic functionality. However, I would
 like to include Unix support at some point in order to broaden the use
 cases as well as this script's potential.

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
