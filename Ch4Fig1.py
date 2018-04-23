import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
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
#Put the eigensystem in decreasing
#order of eigenvalues
sortorder=evals.argsort()[::-1]
evals=evals[sortorder]
evecs=evecs[:,sortorder]

#Make the scree plot
plt.plot(range(1,5), list(evals*100/sum(evals)))
## Configure the graph
plt.title('Scree plot, Currencies 1999-'+lastday[:4])
plt.ylabel('Percent of Trace')
plt.xticks(range(1,5),range(1,5))
plt.grid(True)
plt.show

#Display the 4x4 covariance matrix
print('1999-'+lastday[:4]+' covariance matrix: (%d days)' % len(difflgs))
for i in range(4):
    print(c[i]*10000)

#Compute 2008 covariance matrix
s2008=lgdates.index('2008-01-02')
e2008=lgdates.index('2008-12-31')
c2008=np.cov(np.array(difflgs[s2008-1:e2008+1]).T)
#Display the 4x4 covariance matrix
print('2008 covariance matrix:')
for i in range(4):
    print(c2008[i]*10000)

#Display the eigenvalues
print('Full period eigenvalues:')
print(evals*1000000)

#Display the eigenvectors
print('Eigenvector (column) matrix:')
for i in range(4):
    print(evecs[i])
    
#get eigenvalues and eigenvectors of the 2008 matrix
evals2008,evecs2008=np.linalg.eig(c2008)
#Put the eigensystem in decreasing
#order of eigenvalues
sortorder2008=evals2008.argsort()[::-1]
evals2008=evals2008[sortorder2008]
evecs2008=evecs2008[:,sortorder2008]

#Display the 2008 eigenvalues
print('2008 eigenvalues:')
print(evals2008*1000000)

#Display the 2008 eigenvectors
print('2008 eigenvector (column) matrix:')
for i in range(4):
    print(evecs2008[i])
