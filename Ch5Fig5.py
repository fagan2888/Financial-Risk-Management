import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get Swissies from FRED until the end of
#previous year.

lastday=LastYearEnd()
seriesnames=['DEXSZUS']
cdates,ratematrix=GetFREDMatrix(seriesnames,
            enddate=lastday)

oldstate=np.seterr(all='ignore')
#Convert levels to log-returns
#First take logs of the currency levels
#Swissie and yen are in currency/dollar, but
#the Pound is dollar/currency. Reverse sign
#of the Pound.
multipliers=[-1]  #Just reading the Swissie in this segment
lgrates=[]
for i in range(len(ratematrix)):
    lgrates.append(list(np.log(ratematrix[i])))
    lgrates[i]=list(np.multiply(lgrates[i],multipliers))
#take differences of the logs.
#get rid of any with no data
difflgs=[]
lgdates=[]
idxold=0   #Keeps track of the last good time period
for i in range(1,len(ratematrix)):    
    x=list(np.subtract(lgrates[i],lgrates[idxold]))
    if pd.notna(x[0]):
        difflgs.append(x)
        lgdates.append(cdates[i])
        idxold=i
np.seterr(**oldstate)

#Get block maxima (actually minima since
#looking for big losses) by grouping into
#10-day blocks
chf=[row[0] for row in difflgs]
blocksize=10
worstguys=[]
for i in range(0,len(chf),blocksize):
    #Note sign change so losses are positive    
    worstguys.append(-min(chf[i:i+10]))

#Plot a histogram of block maxima
# the histogram of the data
#Long-tailed to the right so have a "more"
#category
num_bins=int(np.sqrt(len(worstguys))/2)
bestofworst=np.min(worstguys)
prettybad=np.percentile(worstguys,99)
binsize=(prettybad-bestofworst)/num_bins
binlist=np.arange(bestofworst,
          prettybad,binsize)
n, bins, patches = plt.hist(worstguys, 
          bins=binlist, density=1)
plt.title('Block Minima, CHF/USD 1971-'+lastday[:4])
plt.ylabel('Count')
plt.xlabel('Block minimum log-return')
plt.grid()
plt.show
