import matplotlib.pyplot as plt
import random
tenorsfromtsy=[0.083333333,0.25,0.5,1,2,3,5,7,10,20,30]
#Curve source:
#https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield
curve2017=[1.28,1.39,1.53,1.76,1.89,1.98,
           2.2,2.33,2.4,2.58,2.74]
#Interpolate curve monthly

curve=curve2017
curve360=[]
tenors=[]
shortrates=[]
idxtsy=0
mnthtsy=round(tenorsfromtsy[idxtsy]*12)
#Fill in curve360 every month between the knot points
#given in curve
#As curve is filled in, bootstrap a short rate curve
for month in range(360):
    tenors.append(float(month+1)/12)
    if (month+1==mnthtsy):   #Are we at a knot point?
        #Copy over original curve at this point
        curve360.append(curve[idxtsy])
        #Move indicator to next knot point
        idxtsy+=1
        if (idxtsy!=len(tenorsfromtsy)):
            #Set month number of next knot point
            mnthtsy=round(tenorsfromtsy[idxtsy]*12)
    else:   #Not at a knot point - interpolate
        timespread=tenorsfromtsy[idxtsy]-tenorsfromtsy[idxtsy-1]
        ratespread=curve[idxtsy]-curve[idxtsy-1]
        if (timespread<=0):
            curve360.append(curve[idxtsy-1])
        else:
            #compute years between previous knot point and now
            time_to_previous_knot=(month+1)/12-tenorsfromtsy[idxtsy-1]
            proportion=(ratespread/timespread)*time_to_previous_knot
            curve360.append(curve[idxtsy-1]+proportion)
    #Bootstrap a short rate curve
    short=curve360[month]    
    if (month!=0):
        denom=tenors[month]-tenors[month-1]
        numer=curve360[month]-curve360[month-1]
        if (denom!=0):
            short+=tenors[month]*numer/denom
    shortrates.append(short)

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
plt.plot(tenors, curve360, label='Original UST Curve')
plt.plot(tenors, shortrates, label='Original Short Curve')
plt.plot(tenors, randomwalk, label='Sample Short Curve')
plt.plot(tenors, curvesample, label='Sample UST Curve')
## Configure the graph
plt.title('Hull-White Curve Generation')
plt.xlabel('Tenor')
plt.ylabel('Rate')
plt.legend()
plt.grid(True)
plt.show
