import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#Generate 10,000 standard normal draws
#Take exceedances over 2
threshold=2
n=10000
random.seed(314159)

#Using this random number generator
#because we can control the seed
sample=[]
for i in range(n):
    sample.append(random.gauss(0,1))
    
exceeds=[s-threshold for s in sample if s>threshold]

numex=len(exceeds)
avex=np.mean(exceeds)

print('Number of exceedances over {0}: {1}'.format(threshold,numex))
print('Average exceedance:',avex)

#Maximum likelihood function 5.67 with these values
maxlike=-numex*(np.log(avex)+1)
print('Maximum likelihood function at beta,number:',maxlike)

#Show the Q-Q plot
#x's are sorted values of the exceedances
xsample=np.sort(exceeds)
ysample=[(i+1)/(numex+1) for i in range(numex)]
ygumbel=[1-np.exp(-x/avex) for x in xsample]

plt.plot(xsample,ysample,label='Sample')
plt.plot(xsample,ygumbel,label='Gumbel')

plt.grid()
plt.legend()
plt.title('Q-Q plot Gumbel vs. sample of exceedences')
plt.show

#Find best fit of parameters beta and xi
def GPD(x,xi,beta):
    #Cumulative distribution function is
    #1-(1+xi*x/beta)^(-1/xi)
    b=1+xi*x/beta
    return(1-b**(-1/xi))
    
argopt,argc=curve_fit(xsample,ysample,GPD)
