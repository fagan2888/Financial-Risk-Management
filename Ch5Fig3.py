import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
#Generate tail densities for various alpha's
#using formula 5.28a
x=np.arange(4.5,7.1,.1)
beta=0.0
gamma=1.0
alpha=[0.5,1.0,1.2,1.7,1.9]

for i,a in enumerate(alpha):
    tailscale=gamma**a
    tailscale*=np.sin(np.pi*a/2)
    tailscale*=sp.special.gamma(a)/np.pi
    tailscale*=(1+beta)
    row=[tailscale*x**(-a)]
    plt.plot(x,np.array(row[0]),label=str(a))

plt.grid()
plt.legend()
plt.title('Tail densities at various '+r'$\alpha$'+"'s, Formula 5.28a")
plt.show
