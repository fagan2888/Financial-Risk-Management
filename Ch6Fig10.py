import numpy as np
import matplotlib.pyplot as plt
#Draw graph of pseudo-delta functions
xs=np.arange(-5,5.1,.1)
ks=[1,2,4]
for k in ks:
    ys=[1/(1+np.exp(k*x)) for x in xs]
    plt.plot(xs,ys,label='k='+str(k))

plt.legend()
plt.grid()
plt.show()
