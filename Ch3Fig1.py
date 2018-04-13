#Graph an efficient frontier with inefficient
#points below it
import matplotlib.pyplot as plt
import numpy as np

# evenly sampled standard deviation
t = np.arange(0.05, .2, 0.005)

#Plot the frontier
plt.plot(t, .7*(t-.04)**.5-.04, 'bD', color='darkblue')
markers=['o','*','8','s','p','x']
colors=['yellow','red','green','orange','black','magenta']
#Six sets of random inefficient portfolios
for i in range(6):
    s=np.random.uniform(0,1,len(t))
    plt.scatter(t, s*(.7*(t-.04)**.5-.04), marker=markers[i], color=colors[i])
plt.axis([0,.25,0,.3])
plt.title('Efficient Frontier and Inefficient Portfolios')
plt.xlabel('Risk (annual std. deviation)')
plt.ylabel('Reward (arith. annual return)')
plt.grid(True)
plt.show()
