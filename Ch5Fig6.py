#To be run after Ch5Fig5.py

#Find the best fit of the empirical Q-Q
#plot with a parameterized GEV Q-Q
from scipy.optimize import curve_fit
from scipy.special import gamma
xsample=np.sort(worstguys)
ysample=[(i+1)/(n+1) for i in range(n)]

#Find best fit of GEV parameters sigma and xi
#In this case we just try Frechet because
#Weibull makes no sense (limits biggest loss)
#and Gumbel is essentially Frechet with a small xi

def Frechet(x,sigmalog,xilog):
    #Cumulative Generalized Extreme Value
    #distribution function is
    #exp(-(1+xi*(x-mu)/sigma)**(-1/xi))
    #For a Frechet distribution, we enforce
    #sigma and xi positive by taking exp's of the
    #arguments. mu is computed from sigma
    #and xi (see p. 26 of lecture notes)
    sigma=np.exp(sigmalog)
    xi=np.exp(xilog)
    mu=np.mean(x)-sigma*(gamma(1-xi)-1)/xi
    b=1+xi*(x-mu)/sigma
    if np.min(b)<0:
        print('Problem:',np.min(b))
    gevcdf=np.exp(-(b**(-1/xi)))
    return(gevcdf)

#intial guess
xi=.2
sigma=np.std(xsample)
guess=np.array([np.log(sigma),np.log(xi)])

#Get best arguments for Frechet (xi>0) distribution
fargopt,fargc=curve_fit(Frechet,xsample,ysample,guess)

sigma=np.exp(fargopt[0])
xi=np.exp(fargopt[0])
mu=np.mean(xsample)-sigma*(gamma(1-xi)-1)/xi
print('Frechet mu:',mu)
print('Frechet sigma:',sigma)
print('Frechet xi:',xi)

#Make the Q-Q plot of extremes
#versus the best fit Frechet
#Inverse Frechet of a probability p is:
#sigma*{((-ln(p))^(-xi)-1)/xi}+mu
#Equally spaced p's are in ysample
xfrechet=(-np.log(ysample))**(-xi)-1
xfrechet*=sigma/xi
xfrechet+=mu
#Plot the diagonal
line=plt.plot(xfrechet,xfrechet)
plt.setp(line, linewidth=2, color='r')
#Plot the actuals
plt.scatter(xfrechet,xsample, s=40, c='g')
tstr='Q-Q plot, CHF %d-day max loss vs. Frechet, ' % blocksize
tstr+=lgdates[0][:4]+'-'+lastday[:4]
plt.title(tstr)
plt.ylabel('Log-return loss')
plt.grid(True)
plt.show
