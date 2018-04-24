#This code segment to be run after Ch4Fig3.py

#Draw Cornish-Fisher graph
stepsize=12*(np.sqrt(2)-1)/100
x=np.arange(-50*stepsize+.0001,
            50*stepsize,stepsize)
y1=[4*(1+11*(x/6)**2+np.sqrt((x/6)**4-6*(x/6)**2+1))][0]
y2=[4*(1+11*(x/6)**2-np.sqrt((x/6)**4-6*(x/6)**2+1))][0]
x=np.append(x,50*stepsize)
y1=np.append(y1,4*(1+11*(x[100]/6)**2))
y2=np.append(y2,4*(1+11*(x[100]/6)**2))
plt.plot(x,y1)
plt.plot(x,y2)
plt.fill_between(x,y1,y2,facecolor='green')
plt.xlabel('Skewness')
plt.ylabel('Excess Kurtosis')
plt.title('Allowed parameter combinations for Cornish-Fisher')
plt.grid()
plt.show()

#Compute new z-score using 4.85
z=stats.norm.ppf(.99)
znew=z-(1/6)*(z**2-1)*stats.skew(portfolio)
znew+=(z/24)*(z**2-3)*stats.kurtosis(portfolio)
znew-=(z/36)*(2*z**2-5)*stats.skew(portfolio)**2
print('Normal 99%% z: %8.5f' % z)
print('Cornish-Fisher: %8.5f' % znew)
#Show comparisons of VaRs
print('Normal 99%% VaR: %8.5f' % dn_99VaR)
hs_99VaR=np.percentile(portfolio,1)
hs_99VaR*=100
print('Historical 99%% VaR: %8.5f' % hs_99VaR)
cf_99VaR=-dn_mean*100-znew*dn_std
print('Cornish-Fisher 99%% VaR: %8.5f' % cf_99VaR)

#Show the Cholesky decomposition
#of the CHF-GPB-JPY covariance matrix
chol=np.linalg.cholesky(c)
print('Cholesky:\n',chol*100)

#Generate random draws
strial=np.random.normal(0,1,size=[nobs,3])
rtrial=np.matmul(chol,strial.T).T

#Get trial portfolio returns
ptrial=np.matmul(rtrial,w)
statnames,mettrial,tabtrial=StatsTable(ptrial)

print(tabulate(tabtrial))

#Show sample covariance matrix
print('Monte Carlo covariance matrix:')
ctrial=np.cov(rtrial.T)
print(ctrial*10000)
