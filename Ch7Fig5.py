import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from dateutil import parser
#Read in CBOE implied correlation series and form
#constant-maturity series

url='http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/implied_correlation_hist.csv'

dfic=pd.read_csv(url,skiprows=1)

#Form option expiration dates; close enough
#to guess the 19th of January
expiries=[]
for i in range(3,len(dfic.columns)):
    expiries.append(date(int(dfic.columns[i][-4:]),1,19))

#Interpolate current column and next column
offset=408   #New series are created around 408 days to expiration
             #offset gives max weight to new series at 408 days
currcol=3
interpcorr=[]
for i in range(len(dfic)):
    currdate=parser.parse(dfic.DATE[i]).date()
    #Is everything blank?
    if pd.DataFrame.all(pd.isna(dfic.iloc[i,3:])):
        ic=dfic.iloc[i,currcol]  #Leave value blank
    else:
        #Do we need to move to the next series?
        if pd.isna(dfic.iloc[i,currcol]):
            currcol+=1
        #Get bracketing correlations
        try:
            corr1=np.float64(dfic.iloc[i,currcol])
        except ValueError:
            corr1=0
        try:
            corr2=np.float64(dfic.iloc[i,currcol+1])
        except ValueError:
            corr2=0
        #Blank data?
        if corr2==0:
            ic=corr1
        elif corr1==0:
            ic=corr2
        else:
            #Figure weights based on how far from ideal (offset) days
            days1=expiries[currcol-3]-currdate
            days1=np.abs(days1.days-offset)
            days2=expiries[currcol-2]-currdate
            days2=np.abs(days2.days-offset)
            ic=days1*corr2+days2*corr1
            ic/=(days1+days2)
    interpcorr.append(ic)
                                        
#Appears to be a bad data point at 3-Mar-10
badindex=dfic.loc[dfic['DATE']=='3-Mar-10'].index[0]
interpcorr[badindex]=(interpcorr[badindex-1]+interpcorr[badindex+1])/2
    
#interpcorr now has interpolated correlations
#plot them
plt.plot(range(len(interpcorr)),interpcorr)
plt.grid()
plt.title('Constant maturity '+str(offset)+'-day implied correlations, CBOE')
icdates=dfic.DATE
nobs=len(icdates)
stride=int(nobs/48)*12
plt.xticks(range(0,nobs+stride,stride),icdates[0:nobs+stride:stride])
plt.xlim(0,nobs)
plt.ylim(0,100)
plt.show()
