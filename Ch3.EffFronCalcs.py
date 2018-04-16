import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
#Get 4 currencies until the end of
#previous year. Form covariance matrix
#and do simple efficient frontier calculations

lastday=LastYearEnd()
seriesnames=['DEXSZUS','DEXUSEU','DEXUSUK','DEXJPUS']
cdates,ratematrix=GetFREDMatrix(seriesnames,enddate=lastday)

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
mcim=np.matmul(m,np.matmul(ci,m))*10000
print(f'm\'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}m =',mcim*10000,
      'bps')

#Vectors for equation 3.11
u=[1]*3
vec2=np.matmul(ci,u)/uciu
vec1=np.subtract(np.matmul(ci,m)*10000,
                 vec2*ucim)
print('Vector 1 in (3.11):',vec1)
print('Vector 2 in (3.11):',vec2)

lambdacoeff=(uciu*mcim*10000-ucim*ucim)/uciu
constmu=ucim/uciu
print(f'λ\N{SUBSCRIPT ONE} coefficient in μ:',lambdacoeff)
print('Constant term in μ:',constmu,' bps/day')

print(f'1/(u\'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}u) =',1/uciu,
      f'(%/day)\N{SUPERSCRIPT TWO}')

#Draw graph of simple efficient frontier
lambda1s=np.arange(0,1,.01)
xrisk=[]
yreturn=[]
for l1 in lambda1s:
    xrisk.append(np.sqrt(lambdacoeff*l1**2+1/uciu))
    yreturn.append(lambdacoeff*l1+constmu)

plt.figure(1)
plt.plot(xrisk,yreturn,marker='2')
plt.title("Franc, Pound, Yen Efficient Frontier")
plt.xlabel("Standard Deviation (pct/day)")
plt.ylabel("Return (bps/day)")
plt.xlim(0,max(xrisk)+.5)
plt.grid()

print(f'Pound weight goes negative at λ\N{SUBSCRIPT ONE}=',-vec2[1]/vec1[1])
print('At that point μ=',-lambdacoeff*vec2[1]/vec1[1]+constmu,' bps/day')
print('and σ=',np.sqrt(lambdacoeff*(vec2[1]/vec1[1])**2+1/uciu)*100,' bps/day')

#Find the best single investment
ibest=list(m).index(max(m))
#The Euro is still in seriesnames
if ibest==0:
    sn=seriesnames[ibest]
else:
    sn=seriesnames[ibest+1]
print('Best investment was',sn)
print('μ=',m[ibest]*10000,' bps/day')
print('σ=',np.sqrt(c[ibest,ibest])*10000,' bps/day')

#Add a risk-free asset at .1 bps/day
rfrate=.01
plt.figure(2)
plt.plot(xrisk,yreturn,marker='2')
plt.title("Beginning of Franc, Pound, Yen Efficient Frontier")
plt.xlabel("Standard Deviation (pct/day)")
plt.ylabel("Return (bps/day)")
plt.xlim(0,1)
plt.ylim(-.1,2)
plt.annotate('Riskfree asset (0,'+str(rfrate)+')', xy=(0, rfrate),
             xytext=(.2, 1),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
plt.grid()

#Print the tangency portfolio
rfvec=[rfrate]*3
tangencyport=np.matmul(ci,10000*m-rfvec)/(ucim-rfrate*uciu)
print('Tangency portfolio:',tangencyport)
#Solve for the lambda1 at tangency
mutp=np.matmul(tangencyport,m.T)
sigmatp=np.sqrt(np.matmul(np.matmul(tangencyport,c),tangencyport.T))
tpl1=(mutp*10000-constmu)/lambdacoeff
print('TP μ=',mutp*10000,' bps/day')
print('TP σ=',sigmatp*100,' pct/day')
print('lambda1 at tangency:',tpl1)

#Show capital market line
#Extend frontier
lambda1s=np.arange(0,tpl1+.5,.01)
xrisk=[]
yreturn=[]
for l1 in lambda1s:
    xrisk.append(np.sqrt(lambdacoeff*l1**2+1/uciu))
    yreturn.append(lambdacoeff*l1+constmu)

#Compute line
x=np.arange(0,max(xrisk),.01)
y=[]
for r in x:
    y.append(.01*(mutp*10000-rfrate)*r/sigmatp+rfrate)

plt.figure(3)
plt.plot(xrisk,yreturn)
plt.plot(x,y)
plt.annotate('Tangency portfolio', xy=(sigmatp*100, mutp*10000),
             xytext=(1,mutp*10000),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
plt.title("Capital Market Line + Franc, Pound, Yen Efficient Frontier")
plt.xlabel("Standard Deviation (pct/day)")
plt.ylabel("Return (bps/day)")
plt.xlim(0,max(xrisk)+.5)
plt.grid()
plt.show

#Black-Litterman
wmkt=np.array([.05,.15,.8])
mumkt=np.matmul(wmkt,m.T)
varmkt=np.matmul(np.matmul(wmkt,c),wmkt.T)
print('Mkt μ=',mumkt*10000,' bps/day')
print(f'Mkt σ\N{SUPERSCRIPT TWO}=',varmkt*10000,f'(%/day)\N{SUPERSCRIPT TWO}')
betavec=np.matmul(c,wmkt)/varmkt
print('β =',betavec)

mucapm=rfvec+(mumkt*10000-rfrate)*betavec
print('μCAPM=',mucapm,' bps/day')

#View that pounds will outperform yen
view=np.array([0,1,-1])
pview=.00002

gamma=np.matrix([.0001])
sweight=1

#First Black-Litterman matrix calculation
print('C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}/s=',
      10000*ci/sweight)
#Second matrix
v1=np.matmul(np.matrix(view).T,np.linalg.inv(gamma))
vgvmtrx=np.matmul(v1,np.matrix(view))
print('V\'Γ\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}V=',vgvmtrx)
#Sum of the two
print('Sum=',10000*ci/sweight+vgvmtrx)

m1inv=np.linalg.inv(10000*ci/sweight+vgvmtrx)
print('Sum inverse (x10000)=',m1inv*10000)

cimcs=np.matmul(ci,mucapm/sweight)
print('Cinv*muCAPM/s=',cimcs)

print('V\'Γ\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}p=',v1*pview)
m2=cimcs+v1.T*pview
print('Sum=',m2)

mufinal=np.matmul(m1inv,m2.T)*10000
print('Black-Litterman μ:',mufinal)
