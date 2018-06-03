import matplotlib.pyplot as plt
import numpy as np

#3 graohs illustrating lognormal random walks

alpha=.2
sigma=.4
gamma=alpha-(sigma**2)/2
npds=12
periods=np.arange(1,npds+1)

#Graph 1: exponential growth in red
y_exp=np.exp(gamma*(periods-1))
plt.plot(periods,y_exp,color='red')
plt.title("Exponential growth - no stochastic part")
plt.grid()
plt.show()

#Graph 2: random walk in green
r=np.random.normal(0,1,npds)
r=r.cumsum()
y_rwalk=[ye*np.exp(sigma*yr) for (ye,yr) in zip(y_exp,r)]
plt.plot(periods,y_rwalk,color='green')
plt.title("Lognormal random walk")
plt.grid()
plt.show()

#Graph 3: 10 random walks, plus non-random
for i in range(10):
    r=np.random.normal(0,1,npds)
    r=r.cumsum()
    y_rwalk=[ye*np.exp(sigma*yr) for (ye,yr) in zip(y_exp,r)]
    plt.plot(periods,y_rwalk,color='green')

#Put the nonstochastic path in red
plt.plot(periods,y_exp,color='red')
plt.title("10 lognormal random walks, plus nonstochastic path")
plt.grid()
plt.show()
