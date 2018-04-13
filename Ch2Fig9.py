import matplotlib.pyplot as plt
import random
import pandas as pd
#PLot an original (year-end Treasury) curve;
#a short-rate curve based on that;
#a Hull-White randomly generated short-rate curve;
#and a yield curve integrating the Hull-White short curve

#find end of last year
t=pd.Timestamp.now()
for day in [31,30,29,28]:
    lastday=str(t.year-1)+'-12-'+str(day)
    if pd.Timestamp(lastday).weekday()<5:
       break

seriesnames=['DGS1MO','DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
#GetFREDMatrix is in frmbook_funcs
cdates,ratematrix=GetFREDMatrix(seriesnames,startdate=lastday,enddate=lastday)

#Extract numerical (yearly) tenors from series names
tenorsfromtsy=[]
for i in range(len(seriesnames)):
    if seriesnames[i][-2:]=='MO':
        tenorsfromtsy.append(float(seriesnames[i][3:-2])/12)
    else:
        tenorsfromtsy.append(float(seriesnames[i][3:]))

#Get monhtly interpolated curve and short rate curve
tenors,curvemonthly,shortrates=InterpolateCurve(tenorsfromtsy,ratematrix[0])

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
plt.xlabel('Tenor (years)')
plt.ylabel('Rate (%/year)')
plt.legend()
plt.grid(True)
plt.show
