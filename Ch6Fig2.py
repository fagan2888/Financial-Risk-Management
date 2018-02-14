import numpy
import frmbook_funcs

#Get Fama-French market data. Convert to log-returns
Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

#Generate sample standard deviations
SampleSd=[]
Sqrt12=12.0**0.5
for lookback in [12,36,60]:
    Sds=[]  #Save lookback-length SD's in SdS
    for x in range(0,len(ActualReality)-lookback):
        StdDev=numpy.std(\
        ActualReality[x:x+lookback])
        Sds.append(StdDev*Sqrt12)
    SampleSd.append(Sds)   #Add a row to SampleSd

#Graph
StubOffset=6  #First six months are stub dates
lookbacks=[12,36,60]
colors=['y-','b-','r-']
frmbook_funcs.PlotSampleSd('Figure 2',Date,SampleSd,StubOffset,lookbacks,colors)
