#This code segment to be run after Ch4Fig2.py

#Show histogram of equal-weighted
#CHF-GBP-JPY log-changes
w=np.array([1/3]*3).T
portfolio=np.dot(difflgs,w)
#portfolio now contains the equal-weighted portfolio's
#log-returns. Create buckets - hist function doesn't
#seem to have "x or less" or "x or more" buckets
bucketnames=[]
bucketcounts=[]
#Bucket the end percentiles
low1=np.percentile(portfolio,1)
high1=np.percentile(portfolio,99)
bucketnames.append('<=%7.4f' % low1)
bucketcounts.append(sum(1 for x in portfolio if low1 >= x))
#Count 20 even buckets in between low and high
nbucket=20
bucketwidth=(high1-low1)/nbucket
for i in range(20):
    attach=low1+i*bucketwidth
    detach=attach+bucketwidth
    mid=(attach+detach)/2
    bucketnames.append('%7.4f' % mid)
    bucketcounts.append(sum(1 for x in portfolio if (x>=attach and x<=detach)))

#last bucket
bucketnames.append('>=%7.4f' % high1)
bucketcounts.append(sum(1 for x in portfolio if x >= high1))

width=.5
plt.bar(range(nbucket+2),bucketcounts,width)
plt.xticks(range(nbucket+2),bucketnames,rotation='vertical')
plt.grid()
plt.ylabel('Day count')
plt.title('Histogram of equal-weighted CHF+GBP+JPY\n daily log-changes, '+lgdates[0][:4]+'-'+lastday[:4])
plt.show
    
statnames,metrics,table=StatsTable(portfolio)
print(tabulate(table))

#Delta-normal calculations
dn_mean=np.mean(portfolio)   #In fractions
dn_var=np.matmul(np.matmul(w,c),w)*10000   #in (pct/day)**2
print('Delta-Normal Variance %8.4f' % dn_var)
dn_std=np.sqrt(dn_var)    #in pct/day
print('Delta-Normal Standard Deviation %8.4f' % dn_std)
#99% Value at Risk
dn_99VaR=-dn_mean*100-stats.norm.ppf(.01)*dn_std
print('99%% Value at Risk (pct/day): %8.4f' % dn_99VaR)
#Expected Shortfall (4.80)
dn_99ES=np.exp(-.5*stats.norm.ppf(.99)**2)
dn_99ES/=.01*np.sqrt(2*np.pi)
dn_99ES*=dn_std
print('99%% Expected Shortfall (pct/day): %8.4f' % dn_99ES)

#Compute gradient
dn_gradient=1000000*np.matmul(c,w)/dn_std
print('Gradient (bps/day):',dn_gradient)
print('Contributions to Std Dev:',dn_gradient*w)
