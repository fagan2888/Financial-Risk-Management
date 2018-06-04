from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from scipy.stats import norm
import numpy as np

#Assumptions for this graph
k=.5
start_l=2
start_s=1
logterm=np.log((start_s+k)/start_l)
s_factor=start_s/(start_s+k)
time=1
alpha_l=300
alpha_s=-200
rho=.5

def Form9p56(lt,sf,t,alphl,alphs,sl,ss,rh):
    #Compute formula 9.56

    #Compute gamma from 9.52
    biggamma_sq=sl**2+(sf*ss)**2-2*rh*sl*ss*sf
    biggamma_sq/=10000    #convert to fractions from bps
    #Compute B from 9.52
    bigb=alphl-sf*alphs+(sf*ss)**2-rh*sl*ss*sf
    bigb/=10000
    #Compute E1 from 9.52
    e1=(lt-(bigb-biggamma_sq/2)*t)/np.sqrt(biggamma_sq*t)
    #E2 reverses sign of second term in numerator
    e2=(lt+(bigb-biggamma_sq/2)*t)/np.sqrt(biggamma_sq*t)

    failure_prob=norm.cdf(e1)
    failure_prob+=norm.cdf(e2)*np.exp(-logterm*(1-2*bigb/biggamma_sq))
    return(failure_prob)

# Make data.
X = np.arange(.25,30.25,.25)  #Short sigma
Y = np.arange(.25,30.25,.25)  #Long sigma
X, Y = np.meshgrid(X, Y)

#Do Z axis in percent
Z=100.0*Form9p56(logterm,s_factor,time,alpha_l,alpha_s,Y,X,rho)

# Plot the surface.
fig = plt.figure()
ax = fig.gca(projection='3d')
fig.gca().invert_xaxis()

surf = ax.plot_surface(X, Y, Z, cmap=cm.jet,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.01f'))

ax.set_xlabel(r'$\sigma_S$')
ax.set_ylabel(r'$\sigma_L$')
ax.set_zlabel('Failure Prob (%)')
plt.show()
