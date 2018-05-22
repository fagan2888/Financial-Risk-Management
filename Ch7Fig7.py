#To be run after Ch7Fig6.py

InData=np.array(dfeps)

def IntegratedCorrObj(xlam):
    #Compute time series of quasi-correlation
    #matrices from InData using integrated parameter
    #xlam; formula 7.34. Standardize them and apply
    #formula 7.39. Returns scalar 7.39
    #Enforce bounds
    if xlam<0:
        return(10**20)
    elif xlam>.999:
        return(10**20)
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

result=minimize_scalar(IntegratedCorrObj, \
                       bounds=[0,.999])

print('Optimal lambda:',result.x)
print('Optimal objective function:', \
      IntegratedCorrObj(result.x))
print('Half-life (months):',-np.log(2)/np.log(1-result.x))

#Plot integrated correlations
previousq=np.identity(len(InData[0]))
xlam=result.x
rmatrices=[]
for i in range(len(InData)):
    stdmtrx=np.diag([1/np.sqrt(previousq[s,s]) for s in range(len(previousq))])
    rmatrices.append(np.matmul(stdmtrx,np.matmul(previousq,stdmtrx)))
    shockvec=np.mat(np.array(InData[i]))
    #Update q matrix
    shockmat=np.matmul(shockvec.T,shockvec)
    previousq=xlam*shockmat+(1-xlam)*previousq

for it in range(len(tickerlist)-1):
    for jt in range(it+1,len(tickerlist)):
        y=[rmatrices[i][it,jt] for i in range(len(InData))]
        plt.plot(dfeps.index,y,label=tickerlist[it]+'/'+tickerlist[jt])
plt.grid()
xtitle='Integrated correlations λ=%1.5f' % xlam
xtitle+=', '+str(dfeps.index[0])[:4]+'-'+enddate[:4]
plt.title(xtitle)
plt.legend()
plt.show()
