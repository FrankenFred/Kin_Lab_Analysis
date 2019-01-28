import numpy as np
import pandas as pd
import os,sys
import matplotlib.pyplot as plt


Data_DIR = os.getcwd()+"\\" #Data Directory


#Save File info
Save_df = pd.DataFrame(columns=['File','Time','N','AVG_Data','SDEV','SEM'])
Save_file = "AVG_Data.txt"

#Input file info
file_suff = "_CONC.txt" #Suffix of data file


#index of data to strip (if anamolous data)
idx_st = 0
idx_end_init = 0 #set this to < 1 to use end of file


#find all files with "file_suff" end
filelist=[]
for file in os.listdir(Data_DIR):
    if file.endswith(file_suff):
        filelist = np.append(filelist, str(file))

#set up plot...
plot_col = 2
plot_row = int((len(filelist)+plot_col//2)//plot_col)
f, axarr = plt.subplots(plot_row,plot_col, figsize=((plot_col*4),(plot_row*3)))
axarr = axarr.ravel()

for idx, item in enumerate(filelist): #loop through filelist
    
    #import data
    import_df = pd.read_csv(Data_DIR+item,sep='\t',header=None,names=['Time','Data'])
    
	#Trim Data
    if idx_end_init < 1:
        idx_end = len(import_df['Time'])
    elif idx_end_init > len(import_df['Time']):
        idx_end = len(import_df['Time'])
    else: idx_end = idx_end_init
    import_df = import_df[idx_st:idx_end]
	
    import_df['Time'] = import_df['Time']-import_df['Time'][0]
    
    #prep plots
    axarr[idx].plot(import_df['Time'], import_df['Data'], label = str(item))
    axarr[idx].legend(loc="upper right")
    
    Data_AVG = import_df['Data'].mean()
    Data_Stdev = import_df['Data'].std()
    Data_SEM = import_df['Data'].sem()
    Data_Time = import_df['Time'].max()
    Data_N = len(import_df['Time'])
    
    Save_df.loc[idx] = [item,Data_Time,Data_N,Data_AVG,Data_Stdev,Data_SEM]


plt.savefig("Time_Plots.png")

Save_df.to_csv(Data_DIR+Save_file,index=False,sep='\t')






