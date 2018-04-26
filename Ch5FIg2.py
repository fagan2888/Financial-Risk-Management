import numpy as np
import matplotlib.pyplot as plt
#Generate graph comparing Cauchy density
#with normal density
#(formulas 5.27 and 5.26)
x=np.arange(-5,5.2,.2)
gaussmult=1/(2*np.sqrt(np.pi))
ynormal=[gaussmult*np.exp(-x**2/4)]
ycauchy=[1/(np.pi*(1+x**2))]

plt.plot(x,np.array(ynormal[0]),label='Normal')
plt.plot(x,np.array(ycauchy[0]),label='Cauchy')

plt.grid()
plt.legend()
plt.title('Standard Normal (5.26) vs. Cauchy (5.27) density')
plt.show
