import frmbook_funcs
import random
import numpy as np
#Generate virtual reality for graph of standard deviations

#First get actual reality
Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

#Compute overall monthly standard deviation
targetsd=np.std(ActualReality)

#Generate virtual reality with random normal draws with targetsd
VirtualReality=[]
random.seed(3.14159265)
for x in range(len(ActualReality)):
    VirtualReality.append(random.gauss(0,targetsd))

#Generate sample standard deviations for 3 lookback periodicities
lookbacks=[12,36,60]
SampleSd=frmbook_funcs.GenSampleSd(VirtualReality,lookbacks)

#Draw the graph with 3 lines for the 3 periodicities
colors=['y-','b-','r-']
tstr='Figure 1, annual σ=%.2f' % float(targetsd*np.sqrt(12))
frmbook_funcs.PlotSampleSd(tstr,Date,SampleSd,lookbacks,colors)
