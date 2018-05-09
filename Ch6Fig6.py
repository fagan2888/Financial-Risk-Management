import matplotlib.pyplot as plt
#Draw implied vols on two dates by expiry
expiry=[1./52.,1./12.,1./4.,1./2.,1.,2.,3.] 
months=['{0:.2f}'.format(12*e) for e in expiry]
imp2008=[.3612,.3683,.3819,.3750, \
         .3651,.3558,.3555]
imp2010=[.1808,.1874,.2101,.2230, \
         .2335,.2440,.2555]

plt.plot(range(len(expiry)),imp2008,label='20081231',color='r')
plt.plot(range(len(expiry)),imp2010,label='20100802',color='b')
plt.xlabel('Expiry in months')
plt.xticks(range(len(expiry)),months)
plt.title('Implied Vol as a Function of Expiry')
plt.grid()
plt.legend()
plt.show()
