# -*- coding: utf-8 -*-
#Function library for Financial Risk Management book

import numpy
import random
import matplotlib.pyplot as plt

#Generate sample standard deviations over lookback periods
def GenSampleSd(LogReturns,lookbacks):
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
def PlotSampleSd(Title,Date,SampleSd,StubOffset,lookbacks,colors):
    fig, ax = plt.subplots()
    for i, lb in enumerate(lookbacks):
        ax.plot(Date[lb+StubOffset:],
                SampleSd[i][StubOffset:], colors[i],
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
    FFurl='http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'
    r = requests.get(FFurl, allow_redirects=True)
    #Store FF zip file in a temp file
    tmp = tempfile.NamedTemporaryFile(delete=True)
    tmp.write(r.content)
    zf=zipfile.ZipFile(tmp)
    for FFfile in zf.namelist():
        FFdata = zf.read(FFfile)
    tmp.close()  # deletes the temp file
    
    #Split up the Fama-French data (after header) into words
    words=repr(FFdata[162:]).split()
    
    #Parse the Fama-French data
    #dates (YYYYMM format),Mkt-RF,SMB,HML,RF
    Date=[]
    market_minus_rf=[]
    SMB=[]
    HML=[]
    RF=[]
    Date.append(float(words[0][2:8])/100.0)   #Extract first YYYYMM date
    x=1
    while True:
        market_minus_rf.append(float(words[x][0:len(words[x])-1])) 
        SMB.append(float(words[x+1][0:len(words[x+1])-1]))
        HML.append(float(words[x+2][0:len(words[x+2])-1]))
        l3=len(words[x+3])
        try:  #Next period date; this period RF
            NxtDate=int(words[x+3][l3-7:l3-1])  #Generate error if done
            Date.append(float(NxtDate)/100.0)
            RF.append(float(words[x+3][:l3-11]))
            x+=4
        except ValueError: #Last data line; remove returns and newlines
            RF.append(float(words[x+3][:l3-8]))
            break
    #Return the output lists
    return(Date,market_minus_rf,SMB,HML,RF)
#Done with getFamaFrench3

#Change returns in format 5.0=5% to log-returns log(1.05)
#Also add back a risk-free rate
def LogReturnConvert(Ret100,RF):
    LogReturns=[]
    for x in range(len(Ret100)):
        LogReturns.append(100.0*math.log(1+\
        (Ret100[x]+RF[x])/100.))  
    return(LogReturns)
#Done with LogReturnConvert
