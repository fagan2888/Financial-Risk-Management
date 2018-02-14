# -*- coding: utf-8 -*-
#Function library for Financial Risk Management book

#Generate sample standard deviations over lookback periods
def GenSampleSd(LogReturns,lookbacks):
    import numpy
    
    Sqrt12=12.0**0.5
    SampleSd=[]
    for lb in lookbacks:
        Sds=[]    #Save Lookback-length SD's in Sds
        for x in range(len(LogReturns)-lb):
            StdDev=numpy.std(LogReturns[x:x+lb])
            Sds.append(StdDev*Sqrt12)
        SampleSd.append(Sds)   #Add a row to SampleSd
    return(SampleSd)
#Done with GetSampleSd

#Plot a graph of sample standard deviations
def PlotSampleSd(Title,Date,SampleSd,lookbacks,colors):
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()
    for i, lb in enumerate(lookbacks):
        ax.plot(Date[lb:], SampleSd[i], colors[i],\
                label=str(lb)+' month')
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
    legend = ax.legend(loc='upper right', shadow=False, fontsize='medium')
    ax.grid()

    plt.title(Title)
    plt.ylabel('Sample SDs')
    plt.axis([min(Date),max(Date),0,70])
    plt.show()
    return
#Done with PlotSampleSd


#get Fama French 3 factor data from French's website
def getFamaFrench3():
    import pandas as pd
    
    ffurl='http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'

    #Read just the first line of the FF file into a dataframe
    df_monthly = pd.read_csv(ffurl, header=None, nrows=1)
    #Put the line into a string
    str=df_monthly.iloc[0,0]
    #8th word in the string is the last date in the file in YYYYMM format
    lastyear=int(str.split()[8][:4])
    lastmonth=int(str.split()[8][4:])
    #first date in the file is June 1926 - figure out
    #number of months based on that
    periods=(lastyear-1926)*12+(lastmonth-6)    
    
    #Now we know how many periods to read - skip the header and read those monthly periods
    names_monthly = ["yearmon", "mkt_minus_rf", "SMB", "HML", "RF"]
    df_monthly = pd.read_csv(ffurl, skiprows=4, nrows=periods, names=names_monthly)
    
    #Transfer from data frame to output arrays
    Date=df_monthly["yearmon"]
    market_minus_rf=df_monthly["mkt_minus_rf"]
    SMB=df_monthly["SMB"]
    HML=df_monthly["HML"]
    RF=df_monthly["RF"]
    
    return(Date,market_minus_rf,SMB,HML,RF)
#Done with getFamaFrench3

#Change returns in format 5.0=5% to log-returns log(1.05)
#Also add back a risk-free rate
def LogReturnConvert(Ret100,RF):
    import math
    
    LogReturns=[]
    for x in range(len(Ret100)):
        LogReturns.append(100.0*math.log(1+\
        (Ret100[x]+RF[x])/100.))  
    return(LogReturns)
#Done with LogReturnConvert
