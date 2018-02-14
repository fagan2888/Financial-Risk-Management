import numpy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import frmbook_funcs

Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

mu=numpy.average(ActualReality)
sigma=numpy.std(ActualReality)
        
#Generate histogram
minhist=-15
maxhist=15
stepsize=1.5
bins=[]
bins.append(minhist)
for x in range(int((maxhist-minhist)/stepsize)):
    bins.append(bins[x]+stepsize)
            
n, bins, patches = plt.hist(ActualReality, bins, \
                            normed=1, facecolor='blue', alpha=0.5)

# add a 'best fit' line
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y, 'r--')
plt.title(r'Figure 3')
 
# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.show()
