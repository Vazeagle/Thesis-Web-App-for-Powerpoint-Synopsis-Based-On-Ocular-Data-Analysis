import pandas as pd
import csv
import numpy as np
import tkinter
import os

def getResolution():

	#	Get resolution of screen
	root = tkinter.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	return screen_width,screen_height


# Bound the X-axis values based on the screen resolution
def reorganize_dataX( datax, width):
	temp_list = list(map(lambda item: (float(item) + width), datax))
	for index, elem in enumerate(temp_list):
		if float(elem)>width:
			temp_list[index] = width
		elif float(elem)<0:
			temp_list[index] = 0
	temp_list=list(map(float, temp_list)) #convert to float for heatmap
	return temp_list

# Bound the Y-axis values based on the screen resolution
def reorganize_dataY( datay, height):
	temp_list = list(map(lambda item: (float(item) - height), datay))
	for index, elem in enumerate(temp_list):
		if float(elem)>0:
			temp_list[index] = 0
		elif float(elem)<-height:
			temp_list[index] = -height
	temp_list = list(map(lambda item: (float(abs(item))), temp_list))
	temp_list=list(map(float, temp_list)) #convert to float for heatmap
	return temp_list


def registerData(dataFrame):
	resolution = getResolution()
	
	print("Done.")
	print(dataFrame)
	dataX = dataFrame['GazeX'].tolist()
	dataY = dataFrame['GazeY'].tolist()
	print('datatypeforx', type(dataX[0]))


	print("Re-Organize X....")
	dataX = reorganize_dataX(dataX,resolution[0])
	print("Re-Organize Y....")
	dataY = reorganize_dataY(dataY,resolution[1])
	print("width", resolution[0])
	print("height", resolution[1])
	print(dataFrame)
	dataFrame['GazeX'] = dataX
	dataFrame['GazeY'] = dataY

	#	remove timestamp for now because it's unnecessary maybe will use it later on for more info on gaze data
	#final_df = dataFrame.drop('Timestamp', axis=1)
	#print(final_df)
	return dataFrame

def fix_ocular_data():
	#filesLoc = os.getcwd()+"\\ocular_data_csv\\"
	#csvFiles = os.listdir(filesLoc)
	df = pd.read_csv('ocular_data.csv')#Read the csv
	correct_data = registerData(df)
	print("Correcting Ocular Data From User!")
    # Create an empty list
	ocular_data_list = df.values.tolist()
  
    # Iterate over each row
    #for rows in correct_data.iterrows():
    #    # Create list for the current row
    #    my_list =[rows.Timestamp, rows.GazeX, rows.GazeY]
    #    # append the list to the final list
    #    ocular_data_list.append(my_list)

	return ocular_data_list