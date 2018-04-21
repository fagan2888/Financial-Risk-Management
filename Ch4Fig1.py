import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get 4 currencies until the end of
#previous year. Form 4x5 covariance matrix
#and show scree plot of the eigenvalues
#of that matrix

firstday='1999-01-04'
lastday=LastYearEnd()
seriesnames=['DEXSZUS','DEXUSEU','DEXUSUK','DEXJPUS']
cdates,ratematrix=GetFREDMatrix(seriesnames,
            startdate=firstday,enddate=lastday)

oldstate=np.seterr(all='ignore')
#Convert levels to log-returns
#First take logs of the currency levels
#Swissie and yen are in currency/dollar, but
#the other two are dollar/currency. Reverse sign
#of the Euro and Pound.
multipliers=[-1,1,1,-1]
lgrates=[]
for i in range(len(ratematrix)):
    lgrates.append(list(np.log(ratematrix[i])))
    lgrates[i]=list(np.multiply(lgrates[i],multipliers))
#take differences of the logs.
#get rid of any where Yen doesn't have data
difflgs=[]
lgdates=[]
idxold=0   #Keeps track of the last good time period
for i in range(1,len(ratematrix)):    
    x=list(np.subtract(lgrates[i],lgrates[idxold]))
    if pd.notna(x[3]):
        difflgs.append(x)
        lgdates.append(cdates[i])
        idxold=i
np.seterr(**oldstate)

#compute covariance matrix
c=np.cov(np.array(difflgs).T)

#get eigenvalues and eigenvectors
evals,evecs=np.linalg.eig(c)
evals=np.flipud(np.sort(evals))

#Make the scree plot
plt.plot(range(1,5), list(evals*100/sum(evals)))
## Configure the graph
plt.title('Scree plot, Currencies 1999-'+lastday[:4])
plt.ylabel('Percent of Trace')
plt.xticks(range(1,5),range(1,5))
plt.grid(True)
plt.show
