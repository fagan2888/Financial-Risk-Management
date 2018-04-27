import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
#Generate normal tails according to 5.60
xlist=np.arange(0,1.01,.01)
ulist=[2,3,4,5]

for u in ulist:
    fofu=sp.stats.norm.cdf(u)
    y=[(sp.stats.norm.cdf(x+u)-fofu)/(1-fofu) for x in xlist]
    plt.plot(xlist,y,label=str(u))

plt.grid()
plt.legend()
plt.title('Standard Normal Tails (using 5.60)')
plt.show
