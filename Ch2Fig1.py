def formula2p3(c,r,t):
    #Formula 2.3 for price of bond
    #with annual coupon c, t years to
    #maturity, discount rate r
    if r<=-100:  #Unreasonable discount rate
        return(100)
    y=1/(1+r/100)
    price=100*(y**t)
    if (y==1):   #no discount rate
        geometric=t
    else:
        geometric=(1-y**t)/(1-y)
    price+=geometric*c*y
    return(price)
#Done with Formula2p3

import matplotlib.pyplot as plt                                                 
import numpy as np

## Create functions and set domain length
x = np.arange(0, 10.25, .25)
coupon=7
years=29
y=[]
for rate in (x):
    y.append(formula2p3(coupon,rate,years))
plt.plot(x, y)

## Configure the graph
plt.title('Bond Price - Formula 2.3')
plt.xlabel('Discount Rate')
plt.ylabel('Price')
plt.grid(True)
plt.show()
