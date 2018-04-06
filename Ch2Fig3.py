def formula2p9(c,r,t):
    #Formula 2.9 for convexity of bond
    #with annual coupon c, t years to
    #maturity, discount rate r
    if r<=-100:  #Unreasonable discount rate
        return(0)
    y=1/(1+r/100)
    ytothet=y**t
    convexity=100*t*(t+1)*ytothet*(y**2)
    if (y==1):   #no discount rate
        ytttterm=0
    else:
        ytttterm=-(t+1)*(t+2)+2*t*(t+2)*y-t*(t+1)*y**2
        ytttterm*=ytothet
        ytttterm+=2
        ytttterm*=c*(y/(1-y))**3
    convexity+=ytttterm
    #formula2p3 is in Ch2Fig1.py
    price=formula2p3(c,r,t)   #Rescale by price
    convexity/=price
    return(convexity)
#Done with Formula2p9
    
import matplotlib.pyplot as plt                                                 
import numpy as np

## Create functions and set domain length
x = np.arange(0, 14.25, .25)
years=30
baserate=7
#formula2p3 is in Ch2Fig1.py
baseprice=formula2p3(baserate,baserate,years)
#formula2p8 is in Ch2Fig2.py
basedur=formula2p8(baserate,baserate,years)
basecvx=formula2p9(baserate,baserate,years)
y, y1, y2=[], [], []
for rate in (x):
    trueprice=formula2p3(baserate,rate,years)
    durdelta=basedur*(baserate-rate)
    approx1=baseprice+durdelta
    cvxgamma=.5*basecvx*(baserate-rate)**2/100
    approx2=approx1+cvxgamma
    y.append(trueprice)
    y1.append(approx1)
    y2.append(approx2)

plt.plot(x, y, label='True price')
plt.plot(x, y1, label='Dur approx')
plt.plot(x, y2, label='Dur+Cvx approx')
## Configure the graph
plt.title('First and Second Order Approximations')
plt.xlabel('Discount Rate')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
