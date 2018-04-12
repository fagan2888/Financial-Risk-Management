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

def formula2p3(c,r,t):
    #Formula 2.3 for price of bond
    #with annual coupon c, t years to
    #maturity, discount rate r
    if r<=-100:  #Unreasonable discount rate
        return(100)
    y=1/(1+r/100)
    price=100*(y**t)
    if (y==1):   #no discount rate
        geometric=t
    else:
        geometric=(1-y**t)/(1-y)
    price+=geometric*c*y
    return(price)
#Done with Formula2p3

def GetUSCurve(startdate=None,enddate=None):
    #Get US Treasury constant maturity curve from FRED
    #See http://mortada.net/python-api-for-fred.html
    #for information on how to get the FRED (Federal
    #Reserve of St. Louis database) API, and how to get
    #an API key. The key below is Ken Winston's.
    #Returns:
    #    tenors - list of tenors in years
    #    seriesnames - list of FRED series names
    #    cdates - list of yyyy-mm-dd dates
    #    ratematrix - list of time series, one time
    #                 series per tenor
    import pandas as pd
    import numpy
    import fredapi
    fred = fredapi.Fred(api_key='fd97b1fdb076ff1a86aff9b38d7a0e70')
    #Construct Fred series names
    month=1./12.
    tenors=[month,3*month,6*month,1,2,3,5,7,10,20,30]
    seriesnames=['1MO','3MO','6MO','1','2','3','5','7','10','20','30']
    for i,sn in enumerate(seriesnames):
        seriesnames[i]='DGS'+sn
    #Get the time series for each tenor
    #Put them all together in a dataframe
    initialize=True
    for sn in seriesnames:
        print('Processing ',sn)
        fs=fred.get_series(sn,observation_start=startdate, \
                           observation_end=enddate)
        fs=fs.rename(sn)   #put the name on the column
        if initialize:
            #Set up the dataframe with the first series
            dfcurve=pd.DataFrame(fs)
            initialize=False
        else:
            #concatenate the next series to the dataframe
            dfcurve=pd.concat([dfcurve,fs],axis=1)
    
    #The dataframe has aligned the dates
    #strip out date series
    cdates=dfcurve.index.strftime('%Y-%m-%d').tolist()
    ratematrix=[]
    for i in range(len(dfcurve)):
        x=list(dfcurve.iloc[i])
        ratematrix.append(x)
    return(tenors,seriesnames,cdates,ratematrix)
#Done with GetUSCurve

def InterpolateCurve(tenors_in,curve_in):
    #Interpolate curve monthly and return a short
    #rate curve based on the interpolated curve
    #tenors_in has the tenors at the knot points (in years)
    #curve_in has the rate values at the knot point
    #tenors_out has the monthly tenors
    #curve_out has the rates associated with tenors_out
    #shortrates has the bootstrapped short rates
    
    curve_out=[]
    tenors_out=[]
    shortrates=[]
    idxin=0
    mnthin=round(tenors_in[idxin]*12)
    months=round(tenors_in[len(tenors_in)-1]*12)
    #Fill in curve_out every month between the knot
    #points given in curve
    #As curve is filled in, bootstrap a short rate curve
    for month in range(months):
        tenors_out.append(float(month+1)/12)
        if (month+1==mnthin):   #Are we at a knot point?
            #Copy over original curve at this point
            curve_out.append(curve_in[idxin])
            #Move indicator to next knot point
            idxin+=1
            if (idxin!=len(tenors_in)):
                #Set month number of next knot point
                mnthin=round(tenors_in[idxin]*12)
        else:   #Not at a knot point - interpolate
            timespread=tenors_in[idxin]-tenors_in[idxin-1]
            ratespread=curve_in[idxin]-curve_in[idxin-1]
            if (timespread<=0):
                curve_out.append(curve_in[idxin-1])
            else:
                #compute years between previous knot point and now
                time_to_previous_knot=(month+1)/12-tenors_in[idxin-1]
                proportion=(ratespread/timespread)*time_to_previous_knot
                curve_out.append(curve_in[idxin-1]+proportion)
        #Bootstrap a short rate curve
        short=curve_out[month]    
        if (month!=0):
            denom=tenors_out[month]-tenors_out[month-1]
            numer=curve_out[month]-curve_out[month-1]
            if (denom!=0):
                short+=tenors_out[month]*numer/denom
        shortrates.append(short)
        
    return(tenors_out,curve_out,shortrates)
#Done with InterpolateCurve
