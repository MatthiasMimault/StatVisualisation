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
#import os

# 1. Data initialisation and allocation
# Data name
caseName = "A2-T1H8Dp0005"
        
# Get dimensions from stats
CsvStats = pd.read_csv("Csv\\A2-T1H8Dp0005_stats.csv",sep = ";",header=2);
numbFiles = CsvStats.shape[0];
#numbFiles = 10; #debug only with 10 files

# 2. Data reading 2
# Dev
for n in range(0,numbFiles):
# for n in range(99,100):
    # Reading file
    print("Read Csv\\"+caseName+"_"+str(n).zfill(4)+".csv")
    df = pd.read_csv("Csv\\"+caseName+"_"+str(n).zfill(4)+".csv",sep = ";",header=2)
    df = df[['Idp','Pos.x','Qfxx']]
    
    # Compute length
    df['L'] = 2./np.sqrt(df['Qfxx'])
    
    # Bin data
    bins = np.arange(df['Pos.x'].min()-0.025/2, df['Pos.x'].max()+0.025/2,0.025)
    df['PosBin'] = pd.cut(df['Pos.x'], bins, labels = (bins[0:-1]+0.025/2))
        
    # Box plot
    group = df.groupby(['PosBin'])
    plt.scatter((bins[0:-1]+0.025/2), group['L'].mean())
    plt.errorbar((bins[0:-1]+0.025/2), group['L'].mean(), yerr=group['L'].std())
    
    # plt.ylim([df['L'].min(),df['L'].max()])
    plt.ylim([0,0.02])
    
    # Save data and figures
    df.to_csv("Process\\"+caseName+"_"+str(n).zfill(4)+".csv")
    plt.savefig("Png\\"+caseName+"_"+str(n).zfill(4)+".png")
    
    # Clear figure
    plt.clf()