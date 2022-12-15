# Thesis on Web-App Creation For Automating Powerpoint Slides Synopsis Based On Ocular Data Analysis

- Author: Stelios Vazaios

- [List The Data Fields For Cloud Users]
  - [Description](#description)
  - [Purpose](#purpose)
  - [Requirements](#requirements)
  - [Steps](#steps)

## Description

#### General Methodology & Testing:
- Each user of the web app must either be an admin or an user, each one with special rights.
- After configuring the Database to our web app need we need to test it's functionality.
- Test uploading PowerPoint files, and creating  auto synopsis for a test user 
- For the data needed we need to retrieve all the Gaze Data from the eyetracker
- Following that using the python-pptx library we will identify all the powerpoint objects from each slide and do any nessesary modification to them, e.g. split to sub-objects each paragraph(that isn't empty) of a TextBox object and specify their actual borders visible by eye(this means remove margins and empty lines that have no text). These objects must be classified and their exact location and information saved on the database.
- After this we will match each of the user's eytracker data with the powerpoint objects locations.
- Based on this information all objects of the powerpoint will be ranked accordingly.                                                        
- Based on the ranking and the preferences of the user we will create final personalized summary.
- For the summary we must create from the beggining a new MS PowerPoint file and insert the information we want accordingly. The information presented must be edited automatically accordingly to be visually clear and well located on the new slides. 
 &nbsp;
- Due to the multiple features of the MS Powerpoint we have made some rules that the Content Creator must use in order for the software to work as it should and avoid any misbehavior.


## Requirements
- Windows machine with Windows 7 OS and above
- Python 3.8 and above
- IDE like Microsoft Visual Studio Code
- XAMPP or equivalent DB


## Purpose

- Make it easier for a user to recieve crucial information of a presentation by auto-summarizing the most important info based on his ocular data analysis.

## Steps

Use "pip install -r /path/to/requirements.txt" to setup needed packages in the requirement txt
Used Python 3.9.2 whichever version over 3.7 will work too.
The code is still under development and also the libraries are evaluated for their abilities.

#### In Order to run the script successfully:
- Step 1: Connect Tobii EyeTracker 4C to Computer via usb
- Step 2:	Install Tobii's software and calibrate the hardware as per manufacturer instructions
- Step 3:	Use Xampp and import the MySQL-MariaDB database from the repository.
- Step 4: Start the DB Service from Xampp
- Step 5:	Open the Repo as a project dir using and run the app.py
- Step 6:	Connect to the application using 'http://localhost:5002/' from a browser
- Step 7:	Login to the application
- Step 8:	Based on Admin or User Login you have distributed access to the app to use it per preference

<ins>Notes:</ins>

- For this code to work we use TobiiStream.exe which can be downloaded from here: [TobbiStream](http://web.tecnico.ulisboa.pt/~augusto.esteves/GazeTrack/TobiiStream.zip).
