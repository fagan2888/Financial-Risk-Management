#To be run after Ch4Fig1.py has pulled in data

#Make the Q-Q plot of Swiss francs
chf=[row[0] for row in difflgs]
mean=np.mean(chf)
stdev=np.std(chf)
nobs=len(chf)
x=norm.ppf([i/(nobs+1) for i in range(1,nobs+1)])
#Plot the diagonal
line=plt.plot(x, x)
plt.setp(line, linewidth=2, color='r')
#Plot the actuals
y=np.sort(np.array((chf-mean)/stdev))
plt.scatter(x, y, s=40, c='g')
#Find positive outlier
bigplus=max(y)
plt.annotate('January 15, 2015', xy=(max(x), bigplus), xytext=(0, bigplus),
            arrowprops=dict(facecolor='black', shrink=0.02),
            )
bigminus=min(y)
plt.annotate('September 6, 2011', xy=(min(x), bigminus), xytext=(.5*min(x), bigminus),
            arrowprops=dict(facecolor='black', shrink=0.02),
            )
## Configure the graph
plt.title('Q-Q plot, CHF 1999-'+lastday[:4])
plt.ylabel('Standardized Log-return')
plt.grid(True)
plt.show
