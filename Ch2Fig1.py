def formula2p3(c,discount,t):
    #Formula 2.3 for price of bond
    #with annual coupon c, t years to
    #maturity, discount rate discount
    pricevector=[]
    for r in (discount):
        if r<=-100:  #Unreasonable discount rate
            pricevector.append(0)
        else:
            y=1/(1+r/100)
            price=100*(y**t)
            if (y==1):   #no discount rate
                geometric=t
            else:
                geometric=(1-y**t)/(1-y)
            price+=geometric*c*y
            pricevector.append(price)
    return(pricevector)
#Done with Formula2p3

import matplotlib.pyplot as plt                                                 
import numpy as np

## Create functions and set domain length
x = np.arange(0, 10, .25)
coupon=7
years=29
plt.plot(x, formula2p3(coupon,x,years))

## Config the graph
plt.title('Bond Price - Formula 2.3')
plt.xlabel('Discount Rate')
plt.ylabel('Price')
#plt.ylim([0, 4])
plt.grid(True)
## Show the graph
plt.show()
