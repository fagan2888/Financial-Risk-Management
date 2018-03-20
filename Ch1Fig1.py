def CertaintyEquiv(w,p):
    #Certainty equivalent price to pay when current
    #wealth is w for a gamble that pays 1 with probability
    #p and 0 otherwise, log-utility
    if (w<=0) or (p<0) or (p>1):
        return(0)
    tolerance=10**(-10); diff=1/tolerance; c=p
    while abs(diff) > tolerance:
        c2 = w*(1-(1+1/(w+c))**(-p))
        diff = c2-c
        c=c2
    return(c)
#Done with CertaintyEquiv

#Generate isoprobability graphs
import matplotlib.pyplot as plt

wealth=[]
for i in range(100):
    wealth.append(float(i+1)/10)
prob=[]
ceq=[]
for i in range(10):
    prob.append(float(i+1)/10)
    x=[]
    for j in range(100):
        x.append(CertaintyEquiv(wealth[j],prob[i]))
    ceq.append(x)
#ceq now contains a vecor for each of the probabilities;
#the vector has the certainty equivalent value at each wealth

#Plot certainty equivalents in isoprobability lines
fig, ax = plt.subplots()
for i in range(len(prob)):
    ax.plot(wealth,ceq[i])
for label in ax.xaxis.get_ticklabels():
    label.set_rotation(45)
ax.grid()

plt.title('Certainty equivalents - isoprobability')
plt.xlabel('Wealth')
plt.ylabel('Ceq')
plt.axis([min(wealth),max(wealth),0,max(max(ceq))])
plt.show()
