import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#Read time series of implied vol skews
#from csv file and graph them (time and
#moneyness skews)

file='IV skews.csv'
df=pd.read_csv(file)

#Change skew time series from strings to fractions
dates=df['Date']
timeskew=df['Time'].str.rstrip('%').astype('float')/100.0
moneyskew=df['Money'].str.rstrip('%').astype('float')/100.0

#Create a figure whos aspect ratio we can change
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(range(len(timeskew)),timeskew,label='Time')
ax.plot(range(len(moneyskew)),moneyskew,label='Moneyness')

ax.legend(loc='lower center',fontsize=6)
ax.grid()
plt.title('Time and Moneyness IV skews')
plt.xticks(range(0,len(timeskew)+500,500), \
          dates[dates.index % 500 == 0], \
          fontsize=6)
#Figure out size and spacing of y ticks
small=min(min(timeskew),min(moneyskew))
big=max(max(timeskew),max(moneyskew))
plt.yticks(np.arange(small,big+(big-small)/4,(big-small)/4), \
           fontsize=6)

ratio = 0.25   #x axis 4 times y axis
xleft, xright = ax.get_xlim()
ybottom, ytop = ax.get_ylim()
ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
plt.show()
