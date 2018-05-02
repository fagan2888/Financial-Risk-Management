import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get VXO and  VIX from Fred and
#graph them.

lastday=LastYearEnd()
seriesnames=['VXOCLS','VIXCLS']
cdates,ratematrix=GetFREDMatrix(seriesnames,
            enddate=lastday)

#Get rid of double nan's
vols=[]
vdates=[]
for i in range(len(ratematrix)):
    if pd.notna(ratematrix[i][0]) or pd.notna(ratematrix[i][1]):
        vols.append(ratematrix[i])
        vdates.append(cdates[i])

#vols now has VXO and VIX data where at least
#one of them is present.
x=range(len(vdates))
vxo=[row[0] for row in vols]
vix=[row[1] for row in vols]
plt.plot(x,vxo,label='VXO')
plt.plot(x,vix,label='VIX')
plt.title('Figure 4: Implied Volatilities '+vdates[0][:4]+'-'+vdates[len(vdates)-1][:4])

xskip=np.arange(0,len(vdates),1600)
tikskip=[vdates[x][:7] for x in xskip]
plt.xticks(xskip,tikskip)
plt.ylabel('Annual Implied Vol')
plt.legend()
plt.grid()
plt.show
