#To be run after Ch7Fig6.py

InData=np.array(dfeps)

def IntegratedCorrObj(s):
    #Compute time series of quasi-correlation
    #matrices from InData using integrated parameter
    #xlam=exp(s)/(1+exp(s)); note this format removes
    #the need to enforce bounds of xlam being between
    #0 and 1. This is applied to formula 7.34.
    #Standardize Q's and apply formula 7.39.
    #Returns scalar 7.39
    xlam=np.exp(s)
    xlam/=1+xlam
    obj7p39=0
    previousq=np.identity(len(InData[0]))
    #Form new shock matrix
    for i in range(len(InData)):
        #standardize previous q matrix
        #and compute contribution to objective
        #function
        stdmtrx=np.diag([1/np.sqrt(previousq[s,s]) for s in range(len(previousq))])
        previousr=np.matmul(stdmtrx,np.matmul(previousq,stdmtrx))
        #objective function
        obj7p39+=np.log(np.linalg.det(previousr))
        shockvec=np.array(InData[i])
        vec1=np.matmul(shockvec,np.linalg.inv(previousr))
        #This makes obj7p39 into a 1,1 matrix
        obj7p39+=np.matmul(vec1,shockvec)
              
        #Update q matrix
        shockvec=np.mat(shockvec)
        shockmat=np.matmul(shockvec.T,shockvec)
        previousq=xlam*shockmat+(1-xlam)*previousq
    return(obj7p39[0,0])
#Done with IntegratedCorrObj

result=minimize_scalar(IntegratedCorrObj)

xlamopt=np.exp(result.x)
xlamopt/=1+xlamopt
print('Optimal lambda:',xlamopt)
print('Optimal objective function:', \
      result.fun)
if xlamopt>=1 or xlamopt==0:
    halflife=0
else:
    halflife=-np.log(2)/np.log(1-xlamopt)
print('Half-life (months):',halflife)

#Plot integrated correlations
previousq=np.identity(len(InData[0]))
rmatrices=[]
for i in range(len(InData)):
    stdmtrx=np.diag([1/np.sqrt(previousq[s,s]) for s in range(len(previousq))])
    rmatrices.append(np.matmul(stdmtrx,np.matmul(previousq,stdmtrx)))
    shockvec=np.mat(np.array(InData[i]))
    #Update q matrix
    shockmat=np.matmul(shockvec.T,shockvec)
    previousq=xlamopt*shockmat+(1-xlamopt)*previousq

iccol=['r','g','b']
z=0
for it in range(len(tickerlist)-1):
    for jt in range(it+1,len(tickerlist)):
        y=[rmatrices[i][it,jt] for i in range(len(InData))]
        plt.plot(dfeps.index,y, \
            label=tickerlist[it]+'/'+tickerlist[jt], \
            color=iccol[z])
        z+=1
plt.grid()
xtitle='Integrated correlations λ=%1.5f' % xlamopt
xtitle+=', '+str(dfeps.index[0])[:4]+'-'+enddate[:4]
plt.title(xtitle)
plt.legend()
plt.show()

#Map of objective with respect to half-life
halflife=int(halflife)
y=[]
for h in range(halflife-10,halflife+10):
    xlam=1-(.5)**(1/h)
    s=np.log(xlam/(1-xlam))    
    y.append(IntegratedCorrObj(s))
    
plt.plot(range(halflife-10,halflife+10),y)
