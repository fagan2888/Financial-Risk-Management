from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from scipy.stats import norm
import numpy as np

#Assumptions for this graph
ratio=1
start_l=2
start_s=1
logterm=np.log(ratio*start_s/start_l)
time=1
alpha_l=300
alpha_s=-200
rho=.5

def Form9p39(lt,t,alphl,alphs,sl,ss,rh):
    #Compute formula 9.39 (D1) and return cumulative normal of it

    #First compute sigma from 9.37
    bigsigma_sq=sl**2-2*rh*sl*ss+ss**2
    bigsigma_sq/=10000    #convert to fractions from bps
    #Form numerator of D1
    gamma_l=(alphl-sl**2/2)/10000
    gamma_s=(alphs-ss**2/2)/10000
    d1=lt-(gamma_l-gamma_s)*t
    #Divide by denominator
    d1/=np.sqrt(bigsigma_sq*t)
    #d1 is a number of standard deviations.
    #Apply cumulative normal
    return(norm.cdf(d1))

# Make data.
X = np.arange(.25,30.25,.25)  #Short sigma
Y = np.arange(.25,30.25,.25)  #Long sigma
X, Y = np.meshgrid(X, Y)

#Do Z axis in percent
Z=100.0*Form9p39(logterm,time,alpha_l,alpha_s,Y,X,rho)

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
