import numpy as np
import matplotlib.pyplot as plt
#Generate Weibull, Gumbel and Frechet densities
#using 5.42
xlist=np.arange(-2.5,3.55,.05)

xilist=[-0.5,0.0,.5]
namelist=['Weibull','Gumbel','Frechet']

for i,xi in enumerate(xilist):
    y=[]
    for x in xlist:
        if xi!=0:
            opxix=1+xi*x
            if opxix > 0:
                opxixttooxi=opxix**(-1/xi)
                gevcdf=np.exp(-opxixttooxi)
                gevpdf=opxixttooxi*gevcdf/opxix
            else:
                gevcdf=np.nan
                gevpdf=np.nan
        else:  #Gumbel distribution
            gevcdf=np.exp(-np.exp(-x))
            gevpdf=np.exp(-x)*gevcdf
        y.append(gevpdf)    
    plt.plot(xlist,y,label=namelist[i])

plt.grid()
plt.legend()
plt.title('Generalized Extreme Value Densities')
plt.show
