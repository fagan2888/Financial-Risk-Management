import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get 3 currencies until the end of
#previous year. Form 3x3 covariance matrix.
#Show Q-Q plot of CHF
#Print Jarque-Bera statistics
#and normal probability table

lastday=LastYearEnd()
seriesnames=['AAA','BAA','M1333AUSM156NNBR','LTGOVTBD','IRLTCT01USM156N']
cdates,ratematrix=GetFREDMatrix(seriesnames,
            enddate=lastday)

#Splice together the three overlapping long-term
#Treasury series. They agree at the first overlap points
longterm=[x[2] for x in ratematrix[:72]]
longterm+=[x[3] for x in ratematrix[72:492]]
longterm+=[x[4] for x in ratematrix[492:]]

n=len(longterm)

#time series of differences is rough - smooth it
#Roughness probably comes from different timings of
#observations of corporate yields and Treasurys
back=5  #Will take rolling back-month averages
aaa=[x[0]-y for (x,y) in zip(ratematrix,longterm)]
aaamean=np.mean(aaa)
aaa2=np.cumsum(aaa)
aaa3=(aaa2[back:]-aaa2[:-back])/back
aaa=np.concatenate((aaa3, aaa[-back:]), axis=0)  #Fix up the end

bbb=[x[1]-y for (x,y) in zip(ratematrix,longterm)]
bbbmean=np.mean(bbb)
bbb2=np.cumsum(bbb)
bbb3=(bbb2[back:]-bbb2[:-back])/back
bbb=np.concatenate((bbb3, bbb[-back:]), axis=0)

#Show spread time series and straight line for averages
alabel='AAA (avg=%1.2f' % aaamean
alabel+=')'
plt.plot(range(n),aaa,label=alabel,color='blue')
plt.plot(range(n),[aaamean]*n,color='blue')
blabel='BBB (avg=%1.2f' % bbbmean
blabel+=')'
plt.plot(range(n),bbb,label=blabel,color='orange')
plt.plot(range(n),[bbbmean]*n,color='orange')

plt.legend()
plt.grid()
stride=int((n+1)/4)
places=np.arange(0,n+stride,stride)
places[len(places)-1]=n-1
displaydates=[cdates[j][:7] for j in places]    
plt.xticks(places,displaydates)
plt.title("Moody's smoothed yield spreads over Treasurys")
plt.show()
