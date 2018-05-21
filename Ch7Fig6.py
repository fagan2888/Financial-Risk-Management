import intrinio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from frmbook_funcs import LastYearEnd
from frmbook_funcs import Garch11Fit
#Get covariance matrix of 3 stocks from Intrinio

intrinio.client.username = '9de6c0a5ee98c33af8b52bc3396412fb'
intrinio.client.password = 'e2afafa7db68af85ae990dc641a55f79'

#Extract common dates and adjusted closing
#prices; adjusted closes allow total return
#computation

#returns will start one period later than startdate
startdate='1986-12-31'
enddate=LastYearEnd()
tickerlist=['ORCL','ED','F']
for i,t in enumerate(tickerlist):
    #This can be very slow
    print('Getting ticker',t)
    df1=intrinio.prices(t,sort_order='ASC', \
        start_date=startdate,end_date=enddate, \
        frequency='monthly')
    #Get rid of everything except adjusted close
    df1.drop(['adj_high','adj_low','adj_open', \
              'adj_volume','adj_factor','close', \
              'high','low','open','split_ratio', \
              'volume','ex_dividend'],axis='columns',inplace=True)
    df1.rename({'adj_close':t},axis='columns',inplace=True)
    if i==0:
        dfcomb=df1
    else:
        dfcomb=dfcomb.join(df1)

#Combined dataframe dfcomb now has a column
#with adjusted closes of each ticker.
#Form log-returns
nobs=len(dfcomb)-1
for i in range(nobs,0,-1):
    dfcomb.iloc[i]=np.log(dfcomb.iloc[i]/dfcomb.iloc[i-1])
        
#Drop the first row that has the starting prices
dfcomb.drop(dfcomb.index[0],inplace=True)

#Cheat - get overall mean and 
#standard deviation vectors

overallmean=np.mean(dfcomb)
overallstd=np.std(dfcomb)

#Get GARCH params for each ticker
gparams=[]
for it,ticker in enumerate(tickerlist):
    gparams.append(Garch11Fit(initparams,dfcomb[ticker]))
    a,b,c=gparams[it]
    
    #Draw graph
    t=len(dfcomb[ticker])
    minimal=10**(-20)
    stdgarch=np.zeros(t)
    stdgarch[0]=overallstd[ticker]
    #Compute GARCH(1,1) stddev's from data given parameters
    for i in range(1,t):
        #Note offset - i-1 observation of data
        #is used for i estimate of std deviation
        previous=stdgarch[i-1]**2
        var=c+b*previous+\
            a*(dfcomb[ticker][i-1]-overallmean[ticker])**2
        stdgarch[i]=np.sqrt(var)

    #Annualize
    stdgarch*=np.sqrt(12)

    plt.plot(dfcomb.index,stdgarch*100,label=ticker)

plt.grid()
plt.title('GARCH(1,1) fits')
plt.ylabel('GARCH Sample SDs')
plt.legend()
plt.axis([min(dfcomb.index),max(dfcomb.index),0,150])
plt.show()

for it,tick in enumerate(tickerlist):
    print(tick,'a=%1.4f' % gparams[it][0], \
               'b=%1.4f' % gparams[it][1], \
               'c=%1.8f' % gparams[it][2], \
               'AnnEquilibStd=%1.4f' % np.sqrt(12*gparams[it][2]/(1-gparams[it][0]-gparams[it][1])))
