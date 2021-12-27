from pptx import Presentation
import pandas as pd
import numpy as np
import os
import subprocess
import zmq
import tkinter
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
import psutil
from pptx_run import *

#	Get resolution of screen
root = tkinter.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#	Get current working dir
cwd = os.getcwd()
print("Current working directory: ",cwd)
TobiiStream = cwd + "/TobiiStream/TobiiStream.exe"
print(TobiiStream)

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;

processID = None
def startTobiiStream():
	global processID
	# Find PIDs od all the running instances of process that contains 'chrome' in it's name
	listOfProcessIds = findProcessIdByName('TobiiStream')
	if len(listOfProcessIds) > 0:
		print('Process Exists | PID and other details are')
		for elem in listOfProcessIds:
			processID = elem['pid']
			processName = elem['name']
			#processCreationTime =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
			print((processID ,processName))
	else :
		print('No Running Process found with TobiiStream running')
		#open the TobiiStream.exe
		process = subprocess.Popen(TobiiStream, creationflags = subprocess.CREATE_NEW_CONSOLE)
		processID = process.pid


startTobiiStream()








#	DataFrame Initialization
dataSum = pd.DataFrame(columns=['Timestamp','GazeX','GazeY'])

#zmq connection
ctx = zmq.Context()
s = ctx.socket(zmq.SUB)
s.connect("tcp://127.0.0.1:5556")


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


def registerData():
	print("Done.")
	print(dataSum)
	dataX = dataSum['GazeX'].tolist()
	dataY = dataSum['GazeY'].tolist()
	print('datatypeforx', type(dataX[0]))


	print("Re-Organize X....")
	dataX = reorganize_dataX(dataX,screen_width)
	print("Re-Organize Y....")
	dataY = reorganize_dataY(dataY,screen_height)
	print("width", screen_width)
	print("height", screen_height)
	print(dataSum)
	dataSum['GazeX'] = dataX
	dataSum['GazeY'] = dataY

	#	remove timestamp for now because it's unnecessary maybe will use it later on for more info on gaze data
	final_df = dataSum.drop('Timestamp', axis=1)
	print(final_df)
	return dataSum



	#	Set Coordinates for X and Y axis and show heatmap.
	#x = np.array(dataX)
	#y = np.array(dataY)
	#fig, ax = plt.subplots()
	#ax.hist2d(x,y, bins=[np.arange(0,screen_width,1),np.arange(0,screen_height,1)],density=True)
	#ax.set_title('Heatmap based on ocular data')
	#plt.show() #print heatmap

s.setsockopt_string(zmq.SUBSCRIBE,'TobiiStream')


def main():
	index = 0
	result = None
	try:
		while True:
			print("working!!!!!!!!!!")
			msg = s.recv()
			print(msg)
			# Split the (byte) message into 
			split_msg = msg.decode("utf-8").split()
			if split_msg[0] == 'TobiiStream':
				timestamp = split_msg[1]
				eyeX = split_msg[2]
				eyeY = split_msg[3]
				dataSum.loc[index] = [timestamp, eyeX, eyeY] 
				index+=1
				#	check dataSum
				print(dataSum)
				print(TobiiStream)

	except KeyboardInterrupt:#	Ctrl+C
		print("Register the Changes")
		result = registerData()
		gatherData(result)
		#print (result)

		#yPixelStart = 1080
		#yPixelEnd = 0
		#xPixelStart = 0
		#xPixelEnd = 1920
		#objectData = result.loc[(result['GazeY'] <= yPixelStart) & (result['GazeY'] >= yPixelEnd) & (result['GazeX'] >= xPixelStart) & (result['GazeX'] <= xPixelEnd)]
		#print("objData:",objectData)
		#processID.terminate()


main()




###OLD VERSIONS
#process = subprocess.Popen(TobiiStream)

#testing
#process = subprocess.Popen(TobiiStream, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags = subprocess.CREATE_NEW_CONSOLE)

#process = subprocess.Popen(['C:\\windows\\system32\\cmd.exe', '/C', 'C:\Diplomatiki\TobiiStream\TobiiStream.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags = subprocess.CREATE_NEW_CONSOLE)
#process = subprocess.Popen(TobiiStream, stdout=subprocess.PIPE, creationflags = subprocess.CREATE_NEW_CONSOLE)
#process = subprocess.Popen(['runas', '/noprofile', '/user:Administrator',tobiiBat], stdout=subprocess.PIPE, creationflags = subprocess.CREATE_NEW_CONSOLE)