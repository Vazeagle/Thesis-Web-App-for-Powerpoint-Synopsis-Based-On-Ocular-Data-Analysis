import pandas as pd
import csv
import numpy as np
import tkinter
import os, shutil

def getResolution():

	#	Get resolution of screen
	root = tkinter.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()

	return screen_width,screen_height


# Bound the X-axis values based on the screen resolution
def reorganize_dataX( datax, width):
	temp_list = list(map(lambda item: (float(item) - width), datax))
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
	print("Initial not fixed dataframe\n",dataFrame)
	dataFrame['GazeX'] = dataX
	dataFrame['GazeY'] = dataY
	#dataFrame.drop(['Timestamp'], axis=1, inplace=True)

	#	remove timestamp for now because it's unnecessary maybe will use it later on for more info on gaze data
	#final_df = dataFrame.drop('Timestamp', axis=1)
	#print(final_df)
	return dataFrame

def fix_ocular_data(fileName):#fileName is a "smth.csv"
	#temp
	#fileLoc= "raw_csv_data\\"+username+"\\"+"Blockchain_Presentation"+"\\"+fileName
	#delete the above keeep the low
	
	fileLoc = "ocular_data_csv\\"+fileName
	df = pd.read_csv(fileLoc)#Read the csv
	correct_data = registerData(df)
	print("Correcting Ocular Data From User!")
    # Create an list with the dataframe info
	# ocular_data_list = correct_data.values.tolist()
	
	return correct_data	#returns dataframe with correct values!

	#return ocular_data_list #returns a list with fixed data for resolutions!

def handle_ocular_input(newName):
	old_file = os.getcwd()+"\\ocular_data_csv\\ocular_data.csv"
	new_file = os.getcwd()+"\\ocular_data_csv\\"+newName+".csv"

	#if user goes back to a previous slide that already has created a csv file append to that csv file!
	if((os.path.exists(new_file)) and (os.path.exists(old_file))):
		print("Appending new info to the "+newName+".csv file!")
		#read the new file data
		df = pd.read_csv("ocular_data_csv\\ocular_data.csv")#Read the csv
		#Create a list with the csv-dataframe info
		ocular_data_list = df.values.tolist()

		with open('ocular_data_csv/'+newName+'.csv', 'a', encoding='UTF8',newline='') as f:
					writer = csv.writer(f)
					#insert data
					for triplet in ocular_data_list:
						writer.writerow([triplet[0],triplet[1],triplet[2]])
					f.close()
		#delete the ocular_data.csv file
		os.remove(old_file)
	else:
		os.rename(old_file, new_file)
		#if renaming was sucessfull
		if((os.path.exists(new_file)) and not(os.path.exists(old_file))):
			print("File ocular_data.csv successfully renamed to ",newName+".csv")
		#if renaming has failed
		else:
			print("Failed to rename file!")

def deleteOcularData():
	filesLoc = os.getcwd()+"\\ocular_data_csv\\"
	csvFiles = os.listdir(filesLoc)
	for csv in csvFiles:
		print("CSV File to be deleted: ",csv)
		file_path = os.path.join(filesLoc, csv)
		print("file_path delete Ocular Data csv",file_path)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


#Copy the raw eyetracking data for the slides of a powerpoint for usage in metrics etc.
def copy_csv(username,powerpointName):
	copyLoc = os.getcwd()+"\\raw_csv_data\\" + username + "\\" + powerpointName +"\\"
	filesLoc = os.getcwd()+"\\ocular_data_csv\\"
	csvFiles = os.listdir(filesLoc)
	#Check if directory exists and save the images
	if(os.path.exists(copyLoc)):
		#Delete old csv copies to avoid conflict
		copiedCsvFiles = os.listdir(copyLoc)
		for csv in copiedCsvFiles:
			print("CSV File to be deleted: ",csv)
			file_path = os.path.join(copyLoc, csv)
			print("file_path delete Ocular Data csv",file_path)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Failed to delete %s. Reason: %s' % (file_path, e))
		print("Directory: ",copyLoc," already exists !!!")
	else:
		os.makedirs(copyLoc)
		print("Directory: ",copyLoc," created !!!")
	
	
	for csv in csvFiles:
		source = filesLoc + csv
		destination = copyLoc+"\\"+csv
		shutil.copyfile(source, destination)
		print("Copy was Successful")
