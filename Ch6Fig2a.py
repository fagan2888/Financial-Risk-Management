import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import frmbook_funcs

Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

mu=np.average(ActualReality)
sigma=np.std(ActualReality)
        
#Generate histogram
minhist=-15
maxhist=15
stepsize=1.5
bins=np.arange(minhist,maxhist+stepsize,stepsize)
            
n, bins, patches = plt.hist(ActualReality, bins, \
                            facecolor='blue', alpha=0.5)

# add a 'best fit' line
y = norm.pdf(bins,loc=mu,scale=sigma)
y*=np.sum(n)/np.sum(y)
plt.plot(bins, y, 'r--')
plt.title(r'Figure 3')
 
# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.grid()
plt.show()
