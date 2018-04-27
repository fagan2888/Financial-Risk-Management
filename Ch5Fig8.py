import numpy as np
import matplotlib.pyplot as plt
#Generate Generalized Pareto densities
#using 5.65
xlist=np.arange(0,3.05,.05)

#xi=0; density is exp(-x)
plt.plot(xlist,[np.exp(-x) for x in xlist],label='0')

#xi=-.5; upper limit is 2
shortlist=np.arange(0,2.05,.05)
y=[1-x/2 for x in shortlist]
y+=[np.nan]*(len(xlist)-len(shortlist))
plt.plot(xlist,y,label='-.5')

#xi=-1; constant value of 1 up to 1
shortlist=np.arange(0,1.05,.05)
y=[1]*len(shortlist)
y+=[np.nan]*(len(xlist)-len(shortlist))
plt.plot(xlist,y,label='-1')

#xi=-2; blows up at x=.5
#1/sqrt(1-2x)
shortlist=np.arange(0,.5,.05)
y=[1/(1-2*x)**.5 for x in shortlist]
y+=[np.nan]*(len(xlist)-len(shortlist))
plt.plot(xlist,y,label='-2',color='y')

plt.grid()
plt.legend()
plt.title('Generalized Pareto densities using 5.65')
plt.show
