import numpy as np
import matplotlib.pyplot as plt
#Generate mixed normal kurtosis graph
#as in formula 5.19
#x contains fractions of the riskier distribution
#going into the mix
x=np.arange(.05,.5,.05)
#y contains the multiple (how much riskier the
#riskier distribution is than the less risky)  
y=[5,10,15,20]

z=np.zeros((len(y),len(x)))
for i,multiple in enumerate(y):
    for j,mixamount in enumerate(x):
        #Formula 5.19
        z[i,j]= mixamount*multiple**2+1-mixamount
        z[i,j]/=(mixamount*multiple+1-mixamount)**2
        z[i,j]-=1
        z[i,j]*=3
    plt.plot(x,z[i,:],label=str(multiple))

plt.grid()
plt.legend()
plt.xlabel('Fraction of riskier distribution, '+r'$w_1$')
plt.ylabel('Multiple, r')
plt.title('Kurtosis of mixtures of normals, Formula 5.19')
plt.show
