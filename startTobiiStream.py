import subprocess
import os
import signal
import psutil

#	Get current working dir
cwd = os.getcwd()
print("Current working directory: ",cwd)
TobiiStream = cwd + "/TobiiStream/TobiiStream.exe"
print(TobiiStream)
processID = None


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
    return listOfProcessObjects

def startTobiiStream():
    global processID
    # Find PIDs od all the running instances of process that contains 'TobiiStream' in it's name
    listOfProcessIds = findProcessIdByName('TobiiStream')
    if len(listOfProcessIds) > 0:
        print('Process Exists | PID and other details are')
        for elem in listOfProcessIds:
            processID = elem['pid']
            processName = elem['name']
            print((processID ,processName))
        return processID
    else:
        print('No Running Process found with TobiiStream running')
        #open the TobiiStream.exe
        process = subprocess.Popen(TobiiStream, creationflags = subprocess.CREATE_NEW_CONSOLE)
        processID = process.pid
        return processID

def killTobiiStream():
    global processID
    # Find PIDs od all the running instances of process that contains 'TobiiStream' in it's name
    listOfProcessIds = findProcessIdByName('TobiiStream')
    if len(listOfProcessIds) > 0:
        print('Process Exists | PID and other details are')
        for elem in listOfProcessIds:
            processID = elem['pid']
            processName = elem['name']
            print((processID ,processName))
            try:
                os.kill(processID, signal.SIGTERM)
            except:
                print('Cannot kill TobiiStream.exe  process, PID: ',processID)
        return processID
        
    else:
        print('Process TobiiStream.exe does not exist!')