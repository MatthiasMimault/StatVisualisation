# 0. Import detail
# Major lib: numpy (numerics), matplotlib (plot)
# Panda: csv reading
# Seaborn: statistics visualisation
# os: file system manipulations

# Update 05/12/19: Data process to fit Beemster plot format
# Update 10/12/10: Test with Wild card

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.animation as ani
#from numpy import linalg as LA
#import seaborn as sns
import os, fnmatch

# 1. Data initialisation and allocation
# Data name
caseShort = "A3"

# Directory generation
if not os.path.exists("Process"):
    os.mkdir("Process")
if not os.path.exists("Png"):
   os.mkdir("Png")
   
# Wild card test
listOfFiles = os.listdir('Csv\\')
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, "*_stats.csv") and fnmatch.fnmatch(entry, caseShort+"*"):
            print (entry[:-10])
            caseName = entry[:-10]
   
# Get dimensions from stats
CsvStats = pd.read_csv("Csv\\"+caseName+"_stats.csv",sep = ";",header=2);
numbFiles = CsvStats.shape[0];
#numbFiles = 10; #debug only with 10 files

# 2. Data reading
for n in range(CsvStats.Part.min(),CsvStats.Part.max()+1):
    # Reading file
    print("Read Csv\\"+caseName+"_"+str(n).zfill(4)+".csv")
    df = pd.read_csv("Csv\\"+caseName+"_"+str(n).zfill(4)+".csv",sep = ";",header=2)
    df = df[['Idp','Pos.x','GradVel']]
    df['Pos.x'] = df['Pos.x']*1000 #convert mm to um
    df['GradVel'] = df['GradVel']*10 #convert H-1 to %.h-1
    
    # Process Data
    df['Pos.x'] = df['Pos.x'].max()-df['Pos.x']
    
    # Bin data
    bins = np.arange(df['Pos.x'].min()-25/2, df['Pos.x'].max()+25/2,25)
    df['PosBin'] = pd.cut(df['Pos.x'], bins, labels = (bins[0:-1]+25/2))   
        
    # Box plot
    group = df.groupby(['PosBin'])
    plt.scatter((bins[0:-1]+25/2), group['GradVel'].mean())
    plt.errorbar((bins[0:-1]+25/2), group['GradVel'].mean(), yerr=group['GradVel'].std())
    plt.xlim(0, 1700)    
    plt.ylim(0, 150)
    
    
    # plt.ylim([df['L'].min(),df['L'].max()])
    #plt.ylim([-0,0.02])
    
    # Save data and figures
    df.to_csv("Process\\"+caseName+"_"+str(n).zfill(4)+".csv")
    plt.savefig("Png\\"+caseName+"_"+str(n).zfill(4)+".png")
    # Clear figure
    plt.clf()