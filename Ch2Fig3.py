import matplotlib.pyplot as plt                                                 
import numpy as np
#Show a graph of true price of a 7% coupon, 30-year bond
#at different discount rates; compare with duration
#approximation and duration+convexity approximation
x = np.arange(0, 14.25, .25)
years=30
baserate=7
#formula2p3 is in frmbook_funcs
baseprice=formula2p3(baserate,baserate,years)
#formula2p8 is in frmbook_funcs
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
