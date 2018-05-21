import intrinio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from frmbook_funcs import LastYearEnd
#Get covariance and correlation matrix of 3 stocks from Intrinio
#Generate normal Monte Carlo with same correlation,
#and plot samples of correlations from Monte Carlo

intrinio.client.username = '123'  #Get your own username!
intrinio.client.password = '456'  #Get your own password!

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

#Get and show correlation matrix and
#standard deviations
combcorr=dfcomb.corr()
combcov=dfcomb.cov()
combstds=[]
for i in range(len(combcov)):
    combstds.append(np.sqrt(12*combcov.iloc[i,i]))
    
print(combcorr)
print('Annualized standard deviations:\n',combstds)
zsig=np.sqrt(1/(nobs-3))
rsig=(np.exp(2*zsig)-1)/(np.exp(2*zsig)+1)
print('Correlation significance:',rsig)

#Compute minimum variance portfolio (3.13)
covinv=pd.DataFrame(np.linalg.pinv(combcov.values), \
            combcov.columns,combcov.index)
u=pd.Series([1]*len(covinv),index=covinv.index)
minvport=covinv.dot(u)
minvar=1/minvport.dot(u)  #This is second part of formula (3.13)
minvport*=minvar    #This is first part of formula (3.13)
print('Minimum variance portfolio:\n',minvport)

#Annualized standard deviation
annminstd=np.sqrt(minvar*12)
print('Minimum annualized std deviation:',annminstd)

#Generate sampling distribution from multivariate
#normal with correlation matrix combcorr
#Similar to Ch4Fig4.py

#Show the Cholesky decomposition
#of the ORCL-ED-F covariance matrix
chol=np.linalg.cholesky(combcorr)
print('Cholesky:\n',chol*100)

#Generate random draws
nsecs=len(chol)
strial=np.random.normal(0,1,size=[nobs,nsecs])
rtrial=np.matmul(chol,strial.T).T

#Get sample 12-month correlations
samplesize=12
samplecorrs=[]
for i in range(samplesize,nobs+1):
    samplecorrs.append(np.corrcoef(rtrial[i-samplesize:i].transpose()))

#plot sample correlations
sccol=['r','g','b']
ncorrs=nsecs*(nsecs-1)/2
z=0
#Go through each pair
for j in range(nsecs-1):
    for k in range(j+1,nsecs):
        #form time series of sample correlation
        #for this pair of securities
        scs=[samplecorrs[i][j,k] for i in range(nobs-samplesize+1)]
        plt.plot(range(nobs-samplesize+1),scs, \
                 label=dfcomb.columns[j]+'/' \
                 +dfcomb.columns[k], \
                 color=sccol[z])
        #Show target correlation in same color
        line=[combcorr.iloc[j,k]]*(nobs-samplesize+1)
        plt.plot(range(nobs-samplesize+1),line,color=sccol[z])
        z+=1

plt.legend()
scdates=[str(x)[:10] for x in dfcomb.index[samplesize-1:]]
stride=int((nobs-samplesize+1)/(4*samplesize))*samplesize
plt.xticks(range(0,nobs-samplesize+1,stride),scdates[0:nobs-samplesize+1:stride])
plt.title(str(samplesize)+'-month sample correlations, normal Monte Carlo')
plt.grid()
plt.show()
