import matplotlib.pyplot as plt
import numpy as np

#Graph illustrating absorbing barrier

alpha=.2
sigma=.4
gamma=alpha-(sigma**2)/2
npds=12

#Nonstochastic drift part
y_exp=np.exp(gamma*(periods-1))

#Generate walks that are always positive but whose
#difference hits a negative and ends up positive
while True:
    y=[]
    print('trying ys')
    for i in range(2):
        r=np.random.normal(0,1,npds)
        r=r.cumsum()
        y.append([ye*np.exp(sigma*yr) for (ye,yr) in zip(y_exp,r)])
    if min(min(y))>0:
        print('trying z')
        z=[2*y[0][i]+-y[1][i] for i in range(len(y[0]))]
        if min(z)<0 and z[npds-1]>0:
            break

y_long=[2]+[2*y for y in y[0]]
y_short=[1]+y[1]
y_diff=[1]+z
periods=np.arange(0,npds+1)
zeroes=[0]*(npds+1)

#Plot the lines
plt.plot(periods,y_long,color='blue')
plt.plot(periods,y_short,color='yellow')
plt.plot(periods,y_diff,color='red')
plt.plot(periods,zeroes,color='black')

plt.title("Path that goes negative")
plt.grid()
plt.show()
