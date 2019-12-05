# 0. Import detail
# Major lib: numpy (numerics), matplotlib (plot)
# Panda: csv reading
# Seaborn: statistics visualisation
# os: file system manipulations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.animation as ani
#from numpy import linalg as LA
#import seaborn as sns
import os

# 1. Data initialisation and allocation
# Data name
caseName = "A1-Run-GaussianFit"
if not os.path.exists("Process"):
    os.mkdir("Process")
if not os.path.exists("Png"):
   os.mkdir("Png")

        
# Get dimensions from stats
CsvStats = pd.read_csv("Csv\\A1-Run-GaussianFit_stats.csv",sep = ";",header=2);
numbFiles = CsvStats.shape[0];
#numbFiles = 10; #debug only with 10 files

# 2. Data reading 2
# Dev
# for n in range(0,numbFiles):
for n in range(99,100):
    # Reading file
    print("Read Csv\\"+caseName+"_"+str(n).zfill(4)+".csv")
    df = pd.read_csv("Csv\\"+caseName+"_"+str(n).zfill(4)+".csv",sep = ";",header=2)
    df = df[['Idp','Pos.x','Vel.x']]
    df['Pos.x'] = df['Pos.x']*1000
    df['Vel.x'] = df['Vel.x']*100
    
    # Bin data
    bins = np.arange(df['Pos.x'].min()-25/2, df['Pos.x'].max()+25/2,25)
    df['PosBin'] = pd.cut(df['Pos.x'], bins, labels = (bins[0:-1]+25/2))
        
    # Box plot
    group = df.groupby(['PosBin'])
    plt.scatter((bins[0:-1]+25/2), group['Vel.x'].mean())
    plt.errorbar((bins[0:-1]+25/2), group['Vel.x'].mean(), yerr=group['Vel.x'].std())
    
    # plt.ylim([df['L'].min(),df['L'].max()])
    #plt.ylim([-0,0.02])
    
    # Save data and figures
    df.to_csv("Process\\"+caseName+"_"+str(n).zfill(4)+".csv")
    plt.savefig("Png\\"+caseName+"_"+str(n).zfill(4)+".png")
    
    # Clear figure
    plt.clf()