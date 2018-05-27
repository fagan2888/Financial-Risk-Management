import numpy as np
import matplotlib.pyplot as plt

#The data
ratings=['AAA','AA','A','BBB','BB','B','≤CCC']
moodys=[0,.058,.092,.269,1.029,3.191,10.541]
edf2009=[.0093,.0264,.1198,.4393,1.852,10.22,33.904]
indices = [1,2,3,4,5,6,7]
#Calculate optimal width
width = np.min(np.diff(indices))/3

fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(indices-width,moodys,width,color='b',label='-Ymin')
ax.bar(indices,edf2009,width,color='r',label='Ymax')
plt.grid()
plt.xticks(indices,ratings)
plt.yscale('log')
plt.title("Default rates, Moody's historical 1920-2016 and Barclays model 2009")
plt.show()
