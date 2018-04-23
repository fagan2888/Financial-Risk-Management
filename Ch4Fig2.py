import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from tabulate import tabulate
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get 3 currencies until the end of
#previous year. Form 3x3 covariance matrix.
#Show Q-Q plot of CHF
#Print Jarque-Bera statistics
#and normal probability table

lastday=LastYearEnd()
seriesnames=['DEXSZUS','DEXUSUK','DEXJPUS']
cdates,ratematrix=GetFREDMatrix(seriesnames,
            enddate=lastday)

oldstate=np.seterr(all='ignore')
#Convert levels to log-returns
#First take logs of the currency levels
#Swissie and yen are in currency/dollar, but
#the Pound is dollar/currency. Reverse sign
#of the Pound.
multipliers=[-1,1,-1]
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
    if pd.notna(x[2]):
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

#Make the Q-Q plot of Swiss francs
chf=[row[0] for row in difflgs]
mean=np.mean(chf)
stdev=np.std(chf)
nobs=len(chf)
x=stats.norm.ppf([i/(nobs+1) for i in range(1,nobs+1)])
#Plot the diagonal
line=plt.plot(x, x)
plt.setp(line, linewidth=2, color='r')
#Plot the actuals
y=np.sort(np.array((chf-mean)/stdev))
plt.scatter(x, y, s=40, c='g')
#Find positive outlier
bigplus=max(y)
plt.annotate('January 15, 2015', xy=(max(x), bigplus), xytext=(0, bigplus),
            arrowprops=dict(facecolor='black', shrink=0.02),
            )
bigminus=min(y)
plt.annotate('September 6, 2011', xy=(min(x), bigminus), xytext=(.5*min(x), bigminus),
            arrowprops=dict(facecolor='black', shrink=0.02),
            )
## Configure the graph
lgdates
plt.title('Q-Q plot, CHF '+lgdates[0][:4]+'-'+lastday[:4])
plt.ylabel('Standardized Log-return')
plt.grid(True)
plt.show

#Jarque-Bera
sk=stats.skew(chf)
ku=stats.kurtosis(chf)
jb=(nobs/6)*(sk**2+(ku**2)/4)
print('Skewness %f' % sk)
print('Excess Kurtosis %f' % ku)
print('Jarque-Bera Statistic %f' % jb)

#Normal distribution probabilities
print('Normal distribution probabilities (log10)')
for i in range(21):
    print(i,np.log(stats.norm.cdf(-i))/np.log(10))
