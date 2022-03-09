import pandas as pd

#SELECT slide_number, Xcoordinates, Υcoordinates, Τimestamp FROM `ocular_data` WHERE pptx_name='test2' AND username='vazaios' ORDER BY slide_number ASC;



#Get Gaze Data
#Occurrences of pptx object
def getGazeData(dataFrame, paragraphlines, xPixelStart, yPixelStart, lineHeight, LineMargin):   #paragraphlines is an array that has the width of the lines of a paragraph element inside a Textbox #AND ALSO bellow the loop happens for every par so all is ok!!!
    occurrences = 0
    yPixelEnd = yPixelStart - lineHeight - LineMargin
    for lineWidth in paragraphlines:
        xPixelEnd = xPixelStart + lineWidth
        print("getGazeData")
        objectData = dataFrame.loc[(dataFrame['GazeY'] <= yPixelStart) & (dataFrame['GazeY'] >= yPixelEnd) & (dataFrame['GazeX'] >= xPixelStart) & (dataFrame['GazeX'] <= xPixelEnd)]
        print("OCC",occurrences)
        print("DATAFRAMEC:\n",objectData)
        occurrences = len(objectData) + occurrences
    return occurrences