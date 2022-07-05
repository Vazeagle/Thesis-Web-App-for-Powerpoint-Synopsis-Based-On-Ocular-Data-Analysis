import pandas as pd
from ocular_data_handler import *
#SELECT slide_number, Xcoordinates, Υcoordinates, Τimestamp FROM `ocular_data` WHERE pptx_name='test2' AND username='vazaios' ORDER BY slide_number ASC;


#Get Gaze Data
#Occurrences of pptx object
def getGazeData(dataFrame, paragraphlines, xPixelStart, yPixelStart, lineHeight, LineMargin):   #paragraphlines is an array that has the width of the lines of a paragraph element inside a Textbox #AND ALSO bellow the loop happens for every par so all is ok!!!
    print("DATAFRAMEREGISTER!!!!!!: \n",dataFrame)
    occurrences = 0
    Next_yPixelStart = 0
    linecounter = 0
    for lineWidth in paragraphlines:
        linecounter = linecounter + 1
        if linecounter == 1:
            #yPixelStart = yPixelStart
            yPixelEnd = yPixelStart - lineHeight    # in order to get the correct occurrences for each line with correct borders!
            Next_yPixelStart = yPixelEnd - 2*LineMargin
        else:
            yPixelStart = Next_yPixelStart #2* because of the bot and top linespacing!
            yPixelEnd = yPixelStart - lineHeight
            Next_yPixelStart = yPixelEnd - 2*LineMargin
        print("lineWidth:",lineWidth)
        xPixelEnd = xPixelStart + float(lineWidth)#typecast because it gets input as str from the database!
        print("getGazeData")
        objectData = dataFrame.loc[(dataFrame['GazeY'] <= yPixelStart) & (dataFrame['GazeY'] >= yPixelEnd) & (dataFrame['GazeX'] >= xPixelStart) & (dataFrame['GazeX'] <= xPixelEnd)]
        print("OCC",occurrences)
        print("DATAFRAMEC:\n",objectData)
        occurrences = len(objectData) + occurrences
    return occurrences

#IF IMAGE #getGazeData(df, width, image_loc["xAxisStart"], image_loc["yAxisStart"], image_loc["height"], 0)
#IF TEXTBOX #getGazeData(df, parLinesWidth, realXaxisStart, realYaxisStart, yPixelStep, Pixelmargin)