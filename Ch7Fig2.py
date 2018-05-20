#To be run after Ch7Fig1.py
#Copy of code to generate 12-month samples
#Will turn this into a function...

#Get sample 36-month correlations
samplesize=36
samplecorrs=[]
for i in range(samplesize,nobs+1):
    samplecorrs.append(dfcomb.iloc[i-samplesize:i].corr())

#plot sample correlations
sccol=['r','g','b']
ncorrs=nsecs*(nsecs-1)/2
z=0
#Go through each pair
for j in range(nsecs-1):
    for k in range(j+1,nsecs):
        #form time series of sample correlation
        #for this pair of securities
        scs=[samplecorrs[i].iloc[j,k] for i in range(nobs-samplesize+1)]
        plt.plot(range(nobs-samplesize+1),scs, \
                 label=dfcomb.columns[j]+'/' \
                 +dfcomb.columns[k], \
                 color=sccol[z])
        #Show target correlation in same color
        line=[combcorr.iloc[j,k]]*(nobs-samplesize+1)
        plt.plot(range(nobs-samplesize+1),line,color=sccol[z])
        z+=1

plt.legend()
scdates=[str(x)[:10] for x in dfcomb.index[samplesize-1:]]
stride=int((nobs-samplesize+1)/(4*samplesize))*samplesize
plt.xticks(range(0,nobs-samplesize+1,stride),scdates[0:nobs-samplesize+1:stride])
plt.title(str(samplesize)+'-month sample correlations, normal Monte Carlo')
plt.grid()
plt.show()
