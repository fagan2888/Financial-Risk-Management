import matplotlib.pyplot as plt
import random
import pandas as pd
#PLot an original (year-end Treasury) curve;
#a short-rate curve based on that;
#a Hull-White randomly generated short-rate curve;
#and a yield curve integrating the Hull-White short curve
#Use GetUSCurve function in frmbook functions to get Treasury curve
tenorsfromtsy,seriesnames,cdates,ratematrix=GetUSCurve()
#find end of last year
t=pd.Timestamp.now()
for day in [31,30,29,28]:
    lastday=str(t.year-1)+'-12-'+str(day)
    if lastday in cdates:
       break

#Get monhtly interpolated curve and short rate curve
curvefromtsy=ratematrix[cdates.index(lastday)]
tenors,curvemonthly,shortrates=InterpolateCurve(tenorsfromtsy,curvefromtsy)

random.seed(3.14159265)
#set parameters for Ornstein-Uhlenbeck process
#xlambda is spring stiffness; sigma is volatility
xlambda=1
sigma=.05
randomwalk=[]
curvesample=[]
for i,rate in enumerate(shortrates):
    if i==0: # initialize
        randomwalk.append(shortrates[i])
        curvesample.append(randomwalk[i])
    else:
        deterministic=xlambda*(shortrates[i]-randomwalk[i-1])
        #multiply by delta-t
        deterministic*=(tenors[i]-tenors[i-1])
        stochastic=sigma*random.gauss(0,1)
        randomwalk.append(randomwalk[i-1]+deterministic+stochastic)
        #sample curve is average of short rate
        #random walk to this point
        cs=curvesample[i-1]*i
        cs+=randomwalk[i]
        cs/=(i+1)
        curvesample.append(cs)
        
#Plot the four curves      
plt.plot(tenors, curvemonthly, label='UST Curve YE '+str(t.year-1))
plt.plot(tenors, shortrates, label='Short Curve YE '+str(t.year-1))
plt.plot(tenors, randomwalk, label='Sample Short Curve')
plt.plot(tenors, curvesample, label='Sample UST Curve')
## Configure the graph
plt.title('Hull-White Curve Generation')
plt.xlabel('Tenor')
plt.ylabel('Rate')
plt.legend()
plt.grid(True)
plt.show
