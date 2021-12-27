# Thesis on Web-App Creation For Automating Powerpoint Slides Synopsis Based On Ocular Data Analysis

- Author: Stelios Vazaios

- [List The Data Fields For Cloud Users]
  - [Description](#description)
  - [Purpose](#purpose)
  - [Steps](#steps)

## Description

#### Methodology:
- Firstly we need to retrieve all the Gaze Data from the eyetracker
- Following that using the python-pptx library we will identify all the powerpoint objects from each slide and do any nessesary modification to them, e.g. split to sub-objects each paragraph(that isn't empty) of a TextBox object and specify their actual borders visible by eye(this means remove margins and empty lines that have no text).
- After this we will match the eytracker data with the powerpoint objects locations
- Using the matching data and calculating the best data for summary based on the user's ocular data we will create final summary slides 
 &nbsp;
- Due to the multiple features of the MS Powerpoint we have made some rules that the Content Creator must use in order for the software to work as it should and avoid any misbehavior.


## Purpose

- Make it easier for a user to recieve crucial information of a presentation by auto-summarizing the most important info based on his ocular data analysis.

## Steps

Use "pip install -r /path/to/requirements.txt" to setup needed packages in the requirement txt
Used Python 3.9.2 whichever version over 3.7 will work too.
The code is still under development and also the libraries are evaluated for their abilities.

#### In Order to run the script successfully:
- Step 1: Connect Tobii EyeTracker 4C to Computer via usb
- Step 2:	Install Tobii's software and calibrate the hardware as per manufacturer instructions
- Step 3:	Run TobiiStream.exe from TobiiStream file.
- Step 4: Move it to the Same Directory as eye_tracker.py
- Step 5:	Run the eye_tracker.py
- Step 6:	After gathering as much ocular data needed press CTRL + C to interupt and continue the code execution.
- Step 7:	Wait for the data analysis.

<ins>Notes:</ins>

- For this code to work we use TobiiStream.exe which can be downloaded from here: [TobbiStream](http://web.tecnico.ulisboa.pt/~augusto.esteves/GazeTrack/TobiiStream.zip).
