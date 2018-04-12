import matplotlib.pyplot as plt                                                 
import numpy as np
# Plot bond prices using Formula 2.3
# Function formula2p3 is in frmbook_funcs
x = np.arange(0, 14.25, .25)
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
plt.xlim(0,14)
plt.grid(True)
plt.show()
