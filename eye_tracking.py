import pandas as pd
import zmq
import csv

#from pptx_run import *

#signal.signal(signal.CTRL_C_EVENT, signal.default_int_handler)

def recordOcularData(data):
	#ADD IF FOLDER DOESNT EXIST CREATE IT
	#filename=str(time.strftime('%Y-%m-%d %H:%M:%S'))+".csv"
	#filepath="\\ocular_data_csv\\"+filename
	
	#zmq connection
	ctx = zmq.Context()
	s = ctx.socket(zmq.SUB)
	s.connect("tcp://127.0.0.1:5556")
	s.setsockopt_string(zmq.SUBSCRIBE,'TobiiStream')

	#	DataFrame Initialization
	dataSum = pd.DataFrame(columns=['Timestamp','GazeX','GazeY'])

	index = 0
	result = None

	header=['Timestamp','GazeX','GazeY']#BECAUSE WE CANT MAKE IT WORK WITH PARALLEL RUNNING DUE TO SOME LIBRARIES BUGS THIS WILL WORK INSTEAD!
	with open('ocular_data_csv/ocular_data.csv', 'w', encoding='UTF8',newline='') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		f.close()

	try:
		while True:
			print("working!!!!!!!!!!")
			print("TEST DATA IN FUNC:",data)
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
				print("Collectiong Ocular Data to dataframe")
				print("INDEX: ",index)
				with open('ocular_data_csv/ocular_data.csv', 'a', encoding='UTF8',newline='') as f:
					writer = csv.writer(f)
					writer.writerow([timestamp,eyeX,eyeY])
					f.close()
				#dataSum.to_csv('raw_data.csv', index=False)# insert ot every!
				#with open('document.csv','a') as fd:
				#	fd.write(dataSum)
				

	#except InterruptedError:#	Ctrl+C
	except KeyboardInterrupt:	#FOR SOME REASON IT DOESN'T NOT WORK!!!!!!
		print("DataFrame: \n")
		print(dataSum)
		print("\n\n")
		print("Register the Changes")
		print("wont work")
		print("wont work")
		print("wont work")
		print("wont work")
		print("wont work")
		print("wont work")
		print("wont work")
		#time.sleep(10)
		#result = registerData(dataSum)
		#result.to_csv('raw_data.csv', index=False)
		#sys.exit()	#CONTAINS DATAFRAME WITH THE OCULAR DATA WE NEED GazeX GazeY and Timestamp !!!!


		#https://stackoverflow.com/questions/13024532/simulate-ctrl-c-keyboard-interrupt-in-python-while-working-in-linux
		#SOS SOS SOS SOS SOSSOS REMOVE NEXT COMMENT TO WORK!!
		#gatherData(result)
		#print (result)

recordOcularData("testData")