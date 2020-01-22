# 0. Import detail
# Major lib: numpy (numerics), matplotlib (plot)
# Panda: csv reading
# Seaborn: statistics visualisation
# os: file system manipulations

# Update 05/12/19: Data process to fit Beemster plot format
# Update 10/12/19: Test with Wild card
# Update 22/01/20: Average over several files

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.animation as ani
#from numpy import linalg as LA
#import seaborn as sns
import os, fnmatch

# 1. Data initialisation and allocation
# Data name
caseShort = "A0"
SmoothCoef = 4

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
Count = CsvStats['Count'];
Dt = CsvStats['Time'][1]

# Smoothing parameter
print("Number of time step for an hour:"+str(int(0.1/Dt)))
nSmooth = SmoothCoef*int(0.1/Dt);

#numbFiles = 10; #debug only with 10 files

#Bin details
binWidth = 25;
binLength = 1700;

# 2. Data reading
for ns in range(CsvStats.Part.min()+nSmooth,CsvStats.Part.max()+1, int(nSmooth/2)):
    # Smoothed target variable
    bins2 = np.arange(binWidth/2, binLength+binWidth/2,binWidth)
    bins2 = np.append(bins2, binLength+binWidth/2+0.02)
    ser = pd.Series(0, index = range(0, binLength + 1 , binWidth))
    ser = pd.Series(0, index = bins2[:-1])
    err = ser
    print("Read Csv\\"+caseName+"_"+str(ns).zfill(4)+".csv")
    
    # Smoothing subloop
    for n in range(ns-nSmooth,ns+1):
        # Reading file
        df = pd.read_csv("Csv\\"+caseName+"_"+str(n).zfill(4)+".csv",sep = ";",header=2)
        df = df[['Idp','Pos.x','StrainDot.x']]
        
        # Process Data
        df['Pos.x'] = df['Pos.x']*1000 #convert mm to um
        df['Pos.x'] = df['Pos.x'].max()-df['Pos.x']
        
        # Bin data
        df['PosBin'] = pd.cut(df['Pos.x'], bins2-binWidth/2-0.01, labels = bins2[0:-1]) 
        df = df[pd.notnull(df['PosBin'])]
            
        # Box plot
        group = df.groupby(['PosBin'])
        ser = group['StrainDot.x'].mean() + ser
        err = group['StrainDot.x'].std() + err
        
    # Ratio Divided over all per hour (tenth of H) in percentage
    # Strain is m.m-1.h-1
    plt.scatter((bins2[0:-1]+binWidth/2), ser/nSmooth*0.1)
    plt.errorbar((bins2[0:-1]+binWidth/2), ser/nSmooth*0.1, err/nSmooth*0.1)
    plt.xlim(0, binLength)    
    plt.ylim(0, 0.4)    
    
    # Save data and figures
    df.to_csv("Process\\Strain-S"+str(SmoothCoef)+caseName+"_"+str(n).zfill(4)+".csv")
    plt.savefig("Png\\Strain-S"+str(SmoothCoef)+caseName+"_"+str(n).zfill(4)+".png")
    # Clear figure
    plt.clf()