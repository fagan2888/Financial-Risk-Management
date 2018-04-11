import matplotlib.pyplot as plt
import random
import pandas as pd
#PLot 10 Hull-White paths based on yearend US Treasury curve
#Use GetUSCurve function in frmbook functions to get Treasury curve
tenorsfromtsy,seriesnames,cdates,ratematrix=GetUSCurve()
#find end of last year
t=pd.Timestamp.now()
for day in [31,30,29,28]:
    lastday=str(t.year-1)+'-12-'+str(day)
    if lastday in cdates:
       break

curve=ratematrix[cdates.index(lastday)]

#Interpolate curve monthly
#As curve is filled in, bootstrap a short rate curve
curve360=[]
tenors=[]
shortrates=[]
idxtsy=0
mnthtsy=round(tenorsfromtsy[idxtsy]*12)
#Fill in curve360 every month between the knot points
#given in curve
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

#do one graph with sigma=.05 and another
#with sigma=.2
#keep track of range
minrate,maxrate=0,0
subplot=133
for sigma in (.2,.05):
    plt.subplot(subplot)
    print('sigma is',sigma)
    random.seed(3.14159265)
    #set parameters for Ornstein-Uhlenbeck process
    #xlambda is spring stiffness; sigma is volatility
    xlambda=1
    #generate and plot 10 sample curves
    for sample_number in range(10):
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
        minrate=min(curvesample)
        maxrate=max(curvesample)
        plt.plot(tenors,curvesample)

    ## Configure the graph
    plt.title('10 Hull-White Curves, σ='+str(sigma))
    plt.xlabel('Tenor')
    plt.ylabel('Rate')
    plt.ylim(min(0,minrate),max(3,maxrate))
    plt.legend()
    plt.grid(True)
    subplot-=2
    
plt.show
