import matplotlib.pyplot as plt
#Draw implied vols on two dates
moneyness=[.8,.9,1.,1.1,1.2] 
imp2008=[0.510000164, 0.437931821, \
         0.368329438,0.31789782,0.30067243]
imp2010=[0.353624894,0.274183277, \
         0.187416666,0.150996185,0.170348777]

plt.plot(moneyness,imp2008,label='20081231',color='r')
plt.plot(moneyness,imp2010,label='20100802',color='b')
plt.xlabel('Moneyness')
plt.xticks(moneyness,['{:.0%}'.format(m) for m in moneyness])
plt.title('Implied Vol as a Function of Moneyness')
plt.grid()
plt.legend()
plt.show()
