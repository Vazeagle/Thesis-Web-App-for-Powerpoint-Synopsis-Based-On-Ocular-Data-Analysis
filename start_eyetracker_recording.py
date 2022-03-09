import subprocess
#from eye_tracking import *


def start_recording_OcularData():
    print("process1")
    process = subprocess.Popen("python eye_tracking.py", creationflags = subprocess.CREATE_NEW_CONSOLE, stdin=subprocess.PIPE)#, stdout=subprocess.PIPE)#, stderr=subprocess.PIPE)
    #| subprocess.CREATE_NEW_PROCESS_GROUP
    processID = process.pid
    print("process2")
    return process,processID

#We call here this function in order to be able to open it to a different terminal!!
