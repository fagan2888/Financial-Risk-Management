import numpy as np
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get 4 currencies until the end of
#previous year. Form covariance matrix
#and do simple efficient frontier calculations

lastday=LastYearEnd()
seriesnames=['DEXSZUS','DEXUSEU','DEXUSUK','DEXJPUS']
cdates,ratematrix=GetFREDMatrix(seriesnames,enddate='2016-12-30')

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
idxold=0   #Keeps track of the last good time period
for i in range(1,len(ratematrix)):    
    x=list(np.subtract(lgrates[i],lgrates[idxold]))
    if pd.notna(x[3]):
        difflgs.append(x)
        lgdates.append(cdates[i])
        idxold=i
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
print("Means:",m*10000,"bps/day","\n")
print("  ",c[0]*10000)
print("C=",c[1]*10000,"    (3.16)")
print("  ",c[2]*10000)
print(f'(%/day)\N{SUPERSCRIPT TWO} units')
print("  ")
print("From",lgdates[idx],"to",lgdates[len(lgdates)-1])
print("(",len(lgdates),"observations)")

#invert the c matrix
ci=np.linalg.inv(c)/10000
print("    ",ci[0])
print(f'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}=',ci[1],"    (3.17)")
print("    ",ci[2])
print(f'(days/%)\N{SUPERSCRIPT TWO} units')

#For future use
#import from IPython.core.display import Math
#Math(r'$\alpha > \beta$')

#sum entries in ci
uciu=np.sum(ci)
print(f'u\'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}u =',uciu,
      f'(days/%)\N{SUPERSCRIPT TWO}')

ucim=np.sum(np.matmul(ci,m))*10000
print(f'u\'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}m =',ucim,
      'days')

#Vectors for equation 3.11
u=[1]*3
vec2=np.matmul(ci,u)/uciu
vec1=np.subtract(np.matmul(ci,m)*10000,
                 vec2*ucim)
print('Vector 1 in (3.11):',vec1)
print('Vector 2 in (3.11):',vec2)

mcim=np.matmul(m,np.matmul(ci,m))*10000
lambdacoeff=(uciu*mcim*10000-ucim*ucim)/uciu
constmu=ucim/uciu
print(f'λ\N{SUBSCRIPT ONE} coefficient in μ:',lambdacoeff)
print('Constant term in μ:',constmu,' bps/day')

print(f'1/(u\'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}u) =',1/uciu,
      f'(%/day)\N{SUPERSCRIPT TWO}')
