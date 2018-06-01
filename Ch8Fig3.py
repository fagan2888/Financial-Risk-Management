import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get Moody's AAA and BBB yields from FRED.
#Splice together long-term US Treasury rate series,
#and subtract them off to form credit spreads.
#Display and correlate with VIX

lastday=LastYearEnd()
seriesnames=['AAA','BAA','M1333AUSM156NNBR', \
             'LTGOVTBD','IRLTCT01USM156N']
cdates,ratematrix=GetFREDMatrix(seriesnames,
            enddate=lastday)

#Splice together the three overlapping long-term
#Treasury series. They agree at the first overlap points
longterm=[x[2] for x in ratematrix[:72]]
longterm+=[x[3] for x in ratematrix[72:492]]
longterm+=[x[4] for x in ratematrix[492:]]

n=len(longterm)

#Get VIX index which is daily
vxnames=['VXOCLS','VIXCLS']
vxdates,vxmatrix=GetFREDMatrix(vxnames,
            enddate=lastday)
#Align VIX's; monthly dates for bonds look like
#YYYY-MM-01 but they're really the last business day
vixstart=cdates.index(vxdates[0][:8]+'01')
iv=0
for ic in range(vixstart,len(cdates)):
    #New month coming up in VIX series?
    while True:
        usethisguy=(iv==len(vxdates)-1)
        if not usethisguy:
            usethisguy=(vxdates[iv][5:7]!=vxdates[iv+1][5:7])
        if usethisguy:
            #Look for non-NaN
            looking=True
            while looking:
                vix=vxmatrix[iv][1]
                looking=np.isnan(vix)
                if looking:
                    vix=vxmatrix[iv][0]
                    #Are both nan?
                    looking=np.isnan(vix)
                    if looking:
                        iv+=1  #Try next date
            #Found a non-NaN VIX
            #Append VIX value to data
            ratematrix[ic].append(vix)
            iv+=1
            break
        iv+=1

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

#Apply same transform to Treasurys for correlation
tsy2=np.cumsum(longterm)
tsy3=(tsy2[back:]-tsy2[:-back])/back
tsy=np.concatenate((tsy3, longterm[-back:]), axis=0)

#Correlate smoothed spreads with VIX
vix=[x[5] for x in ratematrix[vixstart:]]
av_level=scipy.stats.pearsonr(vix,aaa[vixstart:])[0]
bv_level=scipy.stats.pearsonr(vix,bbb[vixstart:])[0]
av_diff=scipy.stats.pearsonr(np.diff(vix),np.diff(aaa[vixstart:]))[0]
bv_diff=scipy.stats.pearsonr(np.diff(vix),np.diff(bbb[vixstart:]))[0]
print("VIX data starts",cdates[vixstart][:7])
print("AAA/VIX level correlation: %.5f" % av_level)
print("BBB/VIX level correlation: %.5f" % bv_level)
print("AAA/VIX difference correlation: %.5f" % av_diff)
print("BBB/VIX difference correlation: %.5f" % bv_diff)

ab_level=scipy.stats.pearsonr(aaa,bbb)[0]
at_diff=scipy.stats.pearsonr(np.diff(aaa),np.diff(tsy))[0]
bt_diff=scipy.stats.pearsonr(np.diff(bbb),np.diff(tsy))[0]
ab_diff=scipy.stats.pearsonr(np.diff(aaa),np.diff(bbb))[0]
print("Spread and Treasury data starts",cdates[0][:7])
print("AAA/BBB level correlation: %.5f" % ab_level)
print("AAA/Tsy difference correlation: %.5f" % at_diff)
print("BBB/Tsy difference correlation: %.5f" % bt_diff)
print("AAA/BBB difference correlation: %.5f" % ab_diff)

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
