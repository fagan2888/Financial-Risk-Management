from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from scipy.stats import norm
import numpy as np

#Assumptions for this graph
k=.5
logterm1=np.log(k)
start_l=2
start_s=start_l-1
xlambda=(start_l+start_s)/(start_l-start_s)
logterm2=np.log((start_s+k)/start_l)
s_factor=start_s/(start_s+k)
time=1
alpha_l=300
alpha_s=-200
#From 9.61
alpha_lambda=(xlambda+1)*alpha_l/2-(xlambda-1)*alpha_s/2
rho=.5

def Form9p66(lt,xl,t,albda,sl,ss,rh):
    #Compute formula 9.66

    #Compute sigma-lambda
    sigma_lambda_sq=((xl+1)*sl)**2+((xl-1)*ss)**2-2*rh*sl*ss*(xl**2-1)
    sigma_lambda_sq/=40000
    #rescale alpha-lambda from bps
    alf=albda/10000
    #Compute number of standard deviations
    dl1=(lt-(alf-sigma_lambda_sq/2)*t)/np.sqrt(sigma_lambda_sq*t)
    dl2=(lt+(alf-sigma_lambda_sq/2)*t)/np.sqrt(sigma_lambda_sq*t)
    failure_prob=norm.cdf(dl1)
    kpow=np.exp(lt*(2*alf/sigma_lambda_sq-1))
    failure_prob+=kpow*norm.cdf(dl2)
    return(failure_prob)

def Form9p56(lt,sf,t,alphl,alphs,sl,ss,rh):
    #Compute formula 9.56

    #Compute gamma from 9.52
    biggamma_sq=sl**2+(sf*ss)**2-2*rh*sl*ss*sf
    biggamma_sq/=10000    #convert to fractions from bps
    #B from 9.52
    bigb=alphl-sf*alphs+(sf*ss)**2-rh*sl*ss*sf
    bigb/=10000
    #Compute E1 from 9.52
    e1=(lt-(bigb-biggamma_sq/2)*t)/np.sqrt(biggamma_sq*t)
    #E2 reverses sign of second term in numerator
    e2=(lt+(bigb-biggamma_sq/2)*t)/np.sqrt(biggamma_sq*t)
    failure_prob=norm.cdf(e1)
    kpow=np.exp(-lt*(1-2*bigb/biggamma_sq))
    failure_prob+=norm.cdf(e2)*kpow
    return(failure_prob)

# Make data.
X = np.arange(.25,30.25,.25)  #Short sigma
Y = np.arange(.25,30.25,.25)  #Long sigma
X, Y = np.meshgrid(X, Y)

#compute both managed (constant leverage) and unmanaged
#and take difference
Z1=100.0*Form9p56(logterm2,s_factor,time,alpha_l,alpha_s,Y,X,rho)
Z2=100.0*Form9p66(logterm1,xlambda,time,alpha_lambda,Y,X,rho)
Z=Z1-Z2


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
ax.set_zlabel('Failure Prob =Diff (%)')
plt.show()
