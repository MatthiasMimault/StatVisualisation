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
caseShort = "A0"

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
#numbFiles = 10; #debug only with 10 files

# 2. Data reading
for n in range(CsvStats.Part.min(),CsvStats.Part.max()+1):
    # Reading file
    print("Read Csv\\"+caseName+"_"+str(n).zfill(4)+".csv")
    df = pd.read_csv("Csv\\"+caseName+"_"+str(n).zfill(4)+".csv",sep = ";",header=2)
    df = df[['Idp','Pos.x']]
    
    # Process Data
    df['Pos.x'] = df['Pos.x']*1000 #convert mm to um
    df['Pos.x'] = df['Pos.x'].max()-df['Pos.x']
    df = df.assign(In=1, Div=0)
    if (n>1):
        df.loc[df['Idp'] > Count[n-1], 'Div'] = 1
    
    # Bin data
    bins = np.arange(df['Pos.x'].min()-25/2, df['Pos.x'].max()+25/2,25)
    df['PosBin'] = pd.cut(df['Pos.x'], bins, labels = (bins[0:-1]+25/2))   
        
    # Box plot
    group = df.groupby(['PosBin'])
    # Ratio Divided over all per hour (tenth of H) in percentage
    plt.scatter((bins[0:-1]+25/2), (group['Div'].sum()/group['In'].sum())*Dt*10)
    # plt.scatter((bins[0:-1]+25/2), group['GradVel'].mean())
    # plt.errorbar((bins[0:-1]+25/2), group['GradVel'].mean(), yerr=group['GradVel'].std())
    plt.xlim(0, 1700)    
    plt.ylim(0, 0.06)    
    
    # Save data and figures
    df.to_csv("Process\\"+caseName+"_"+str(n).zfill(4)+".csv")
    plt.savefig("Png\\"+caseName+"_"+str(n).zfill(4)+".png")
    # Clear figure
    plt.clf()