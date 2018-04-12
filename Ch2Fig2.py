import matplotlib.pyplot as plt                                                 
import numpy as np
#Plot duration of a newly issued bullet bond
#with same coupon and discount rate
x = np.arange(0, 14.25, .25)
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
plt.xlim(0,14)
plt.grid(True)
plt.show()
