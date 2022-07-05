from ocular_data_handler import *
import os
import os.path
import mss
from PIL import Image, ImageOps


import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import seaborn as sns

def slide_screenshot(slideNum,username,powerpointName):
    slideNum=str(slideNum)

    picSaveLoc= os.getcwd() + "\\heatmaps\\" + username + "\\" + powerpointName + "\\" 
    imgSave = picSaveLoc + slideNum + "_" + powerpointName + ".png"
    
    #Check if directory exists and save the images
    if(os.path.exists(picSaveLoc)):
        print("Directory: ",picSaveLoc," already exists !!!")
    else:
        os.makedirs(picSaveLoc)
        print("Directory: ",picSaveLoc," created !!!")
    
    #take screenshot of monitor 2 "mon=2"
    with mss.mss() as sct:
        image = sct.shot(mon=2, output=imgSave)
        #image = sct.shot(mon=2, output=slideNum + ".png")
        print(image)




def plot_heatmap(sldNum,username,powerpointName,df):

    folderLoc= os.getcwd() + "\\heatmaps\\" + username + "\\" + powerpointName + "\\" # maybe a new file for the specific powerpoint?

    slideNum = str(sldNum)#get the slide number by splitting the _ of the name of the picture

    #if folder exists
    if(os.path.exists(folderLoc)):
        #list dir and get only the specific one powerpoint images!
        curpptxPic = slideNum + "_" + powerpointName + ".png"

        resolution = getResolution()

        imagePath = folderLoc + curpptxPic
        map_img = Image.open(imagePath)
        #map_img = map_img.rotate(180)
        map_img = ImageOps.flip(map_img)  

        df.drop(['Timestamp'], axis = 1)

        # Custom it with the same argument as 1D density plot
        hmax = sns.kdeplot(x=df.GazeX, y=df.GazeY, cmap="Reds", shade=True, bw =.15, alpha=0.3)
        hmax.collections[0].set_alpha(0)

        #clear the plot to not overlap.

        ax = plt.gca()
        ax.set_xlim([0, resolution[0]])
        ax.set_ylim([0, resolution[1]])

        imgSave = folderLoc + slideNum + "_" + powerpointName + ".png"

        plt.imshow(map_img, zorder=0)
        plt.savefig(imgSave, bbox_inches='tight')
        plt.close()
    else:
        print("Error, No Slide Screenshots Exist!")


#to be used by admin in order to extract heatmaps for a specific user.
def create_heatmap(username, powerpointName):
    csvFiles = os.listdir(os.getcwd()+"\\raw_csv_data\\"+username+"\\"+powerpointName+"\\")
    for csv in csvFiles:
        slideNumber= int(csv.rsplit('.', 1)[0])
        data_frame = fix_ocular_data(username,csv)
        plot_heatmap(slideNumber,username,powerpointName,data_frame)

#https://stackoverflow.com/questions/50091591/plotting-seaborn-heatmap-on-top-of-a-background-picture

#https://seaborn.pydata.org/generated/seaborn.kdeplot.html

#create_heatmap("testuser12", "Blockchain_Presentation")