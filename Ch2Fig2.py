def formula2p8(c,r,t):
    #Formula 2.8 for Macauley duration of bond
    #with annual coupon c, t years to
    #maturity, discount rate r
    if r<=-100:  #Unreasonable discount rate
        return(0)
    y=1/(1+r/100)
    ytothet=y**t
    duration=100*t*ytothet
    if (y==1):   #no discount rate
        multiplier=t*(t+1)/2
    else:
        multiplier=(1-ytothet-t*(1-y)*ytothet)/(1-y)**2
    duration+=multiplier*c*y
    #formula2p3 is in Ch2Fig1.py
    price=formula2p3(c,r,t)   #Rescale by pricve
    duration/=price
    return(duration)
#Done with Formula2p8
    
import matplotlib.pyplot as plt                                                 
import numpy as np

## Create functions and set domain length
x = np.arange(0, 10.25, .25)
years=30
y=[]
for rate in (x):
    coupon=rate
    y.append(formula2p8(coupon,rate,years))
plt.plot(x, y)

## Configure the graph
plt.title('Duration - Formula 2.8')
plt.xlabel('Discount Rate')
plt.ylabel('Duration')
plt.grid(True)
plt.show()
