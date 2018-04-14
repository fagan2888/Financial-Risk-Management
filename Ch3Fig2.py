#Get 4 currencies
seriesnames=['DEXSZUS','DEXUSEU','DEXUSUK','DEXJPUS']
cdates,ratematrix=GetFREDMatrix(seriesnames)

oldstate=np.seterr(all='ignore')
#Convert levels to log-returns
#First take logs of the currency levels
#Swissie and yen are in currency/dollar, but
#the other two are dollar/currency. Reverse sign
#of the Euro and Pound.
multipliers=[-1,1,1,-1]
lgrates=[]
for i in range(len(ratematrix)):
    lgrates.append(list(np.log(ratematrix[i])))
    lgrates[i]=list(np.multiply(lgrates[i],multipliers))
#take differences of the logs.
#get rid of any where Yen doesn't have data
difflgs=[]
lgdates=[]
for i in range(1,len(ratematrix)):    
    x=list(np.subtract(lgrates[i],lgrates[i-1]))
    if pd.notna(x[3]):
        difflgs.append(x)
        lgdates.append(cdates[i])
np.seterr(**oldstate)

#compute covariance matrix
idx=0
#Euro doesn't start until later
#idx=lgdates.index('1999-01-04')
#Not using Euro - delete column 1
d=np.delete(np.array(difflgs[idx:]),1,1)
c=np.cov(d.T)

#Take the means
m=np.mean(d,axis=0)

#display the output
np.set_printoptions(precision=4)
print("Means:",m*10000,"\n")
print("  ",c[0]*10000)
print("C=",c[1]*10000,"    (3.16)")
print("  ",c[2]*10000)
print("  ")
print("From",lgdates[idx],"to",lgdates[len(lgdates)-1])
print("(",len(lgdates),"observations)")
