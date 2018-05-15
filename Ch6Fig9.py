import frmbook_funcs
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np

#Generate GARCH(1,1) vols from stock market data
#Get Fama-French market data. Convert to log-returns
Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

def GarchMaxLike(params):
    #Implement formula 6.42
    a,b,c=params
    t=len(ActualReality)
    minimal=10**(-20)
    vargarch=np.zeros(t)

    #CHEATS!
    #Seed the variance with the whole-period variance
    #In practice we would have to have a holdout sample
    #at the beginning and roll the estimate forward.
    vargarch[0]=np.var(ActualReality)

    #Another cheat: take the mean over the whole period
    #and center the series on that. Hopefully the mean
    #is close to zero. Again in practice to avoid lookahead
    #we would have to roll the mean forward, using only
    #past data.
    overallmean=np.mean(ActualReality)

    #Compute GARCH(1,1) var's from data given parameters
    for i in range(1,t):
        #Note offset - i-1 observation of data
        #is used for i estimate of variance
        vargarch[i]=c+b*vargarch[i-1]+\
        a*(ActualReality[i-1]-overallmean)**2
        if vargarch[i]<=0:
            vargarch[i]=minimal

    #sum logs of variances
    logsum=np.sum(np.log(vargarch))
    
    #sum yi^2/sigma^2
    othersum=0
    for i in range(t):
        othersum+=((ActualReality[i]-overallmean)**2)/vargarch[i]

    #Actually -2 times (6.42) since we are minimizing
    return(logsum+othersum)

#Starting guess
initparams=[.12,.85,.6]
#Constraint - a+b<1
#first: type of constraint is inequality;
#function defining constraint .9999-a-b
#must be kept positive
#second: same, keep parameters positive
garch_constraints = ({'type': 'ineq', \
                      'fun': lambda x: \
                      .9999-x[0]-x[1]},
                     {'type': 'ineq', \
                      'fun': lambda x: \
                      min(x[0],x[1],x[2])})

results = minimize(GarchMaxLike, \
        initparams, \
        constraints=garch_constraints, \
        method='COBYLA')

#Display results
a,b,c=results.x
print("a=%.3f" % a)
print("b=%.3f" % b)
print("c=%.3f" % c)

#Draw graph
t=len(ActualReality)
minimal=10**(-20)
stdgarch=np.zeros(t)
stdgarch[0]=np.std(ActualReality)
overallmean=np.mean(ActualReality)
#Compute GARCH(1,1) stddev's from data given parameters
for i in range(1,t):
    #Note offset - i-1 observation of data
    #is used for i estimate of std deviation
    previous=stdgarch[i-1]**2
    var=c+b*previous+\
        a*(ActualReality[i-1]-overallmean)**2
    stdgarch[i]=np.sqrt(var)

#Annualize
stdgarch*=np.sqrt(12)

#Just show years
Year=[d/100 for d in Date]
    
plt.plot(Year,stdgarch)
plt.grid()
plt.title('GARCH(1,1) fit to US stock market data')
plt.ylabel('GARCH Sample SDs')
plt.axis([min(Year),max(Year),0,70])
plt.show()
