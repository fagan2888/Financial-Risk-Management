def CertaintyEquiv(w,p):
    #Certainty equivalent price to pay when current
    #wealth is w for a gamble that pays 1 with probability
    #p and 0 otherwise, log-utility
    if (w<=0) or (p<0) or (p>1): #Can't bet anything
        return(0)
    if (p==1):              #Sure thing but can't borrow
        return(min(1,w))    #so only bet what you have up to max
    tolerance=10**(-10); diff=1/tolerance; c=p
    if w <= p:
        c=w/2
    while abs(diff) > tolerance:
        if w <= c:   #Don't have enough wealth to bet fully
            return(w)
        c2 = w*(1-(1+1/(w-c))**(-p))
        diff = c2-c
        c=c2
    return(c)
#Done with CertaintyEquiv

#Generate isoprobability graphs
import matplotlib.pyplot as plt

wealth=[]
for i in range(100):
    wealth.append(float(i+1)/20)
prob=[]
ceq=[]
for i in range(10):
    prob.append(float(i+1)/10)
    x=[]
    for j in range(len(wealth)):
        x.append(CertaintyEquiv(wealth[j],prob[i]))
    ceq.append(x)

fig, ax = plt.subplots()
for i in range(len(prob)):
    ax.plot(wealth,ceq[i])
for label in ax.xaxis.get_ticklabels():
    label.set_rotation(45)
ax.grid()

plt.title('Certainty equivalents - isoprobability')
plt.xlabel('Wealth')
plt.ylabel('Ceq')
plt.axis([min(wealth),max(wealth),0,1])
plt.show()
