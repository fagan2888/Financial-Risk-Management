#Display bar charts with investment grade and speculative
#grade defaults year by year
#Data from Moody's Corporate Default and Recovery Rates,
#1920-2017, Exhibit 30
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

yearrange=np.arange(1920,2018)

moodys={'invt' : pd.Series([ \
0.427,0.387,0.506,0.244,0.14,0.321,0.188, \
0.069,0,0.242,0.151,0.502,0.861,0.79,0.586, \
1.285,0.482,0.619,1.55,0.412,0.592,0,0, \
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, \
0,0,0,0,0,0,0,0.271,0,0,0.232,0,0,0, \
0.11,0,0,0,0,0.214,0,0.175,0,0.211, \
0,0,0.254,0.06,0.059,0,0,0,0,0,0,0.03,0.032, \
0.126,0.124,0.431,0,0,0.061,0,0,0.627,0.428, \
0.095,0.187,0.033,0.096,0.063,0,0,0], index=yearrange), \
'spec' : pd.Series([ \
3.009,2.15,1.762,1.704,2.852,2.562,1.909, \
1.831,0.877,1.401,2.204,7.897,10.989,15.709, \
5.897,6.253,2.72,2.749,2.599,1.774,3.562, \
1.713,0.736,0.615,0.666,0.564,0,0.636,0,1.926, \
0,0.433,0,0,0.467,0.518,0,0.448,0,0,0.75,\
1.072,1.516,1.152,0,0,0.439,0,0.375,0,8.678, \
1.155,1.922,1.28,1.332,1.742,0.868,1.36,1.823, \
0.435,1.63,0.698,3.553,4.061,3.13,3.773,6.163, \
4.31,3.85,5.91,10.54,9.096,4.933,3.404, \
2.341,3.063,1.651,1.889,3.028,5.361,6.074, \
9.634,7.663,5.33,2.418,1.721,1.669,0.945, \
5.426,12.11,3.013,1.982,2.756,2.625,1.938, \
3.67,4.45,2.91], index=yearrange)}

mdf=pd.DataFrame(moodys)

fig=plt.figure() # Create matplotlib figure

#Set up two axes because of different orders of
#magnitude between IG and HY
ax = fig.add_subplot(111)
ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.

width = 0.4

mdf.invt.plot(kind='bar', color='green', ax=ax, width=width, position=1)
mdf.spec.plot(kind='bar', color='blue', ax=ax2, width=width, position=0)

ax.set_ylabel('Investment Grade', color='green')
ax2.set_ylabel('Speculative', color='blue')

#Only show year labels every tick_spacing years
tick_spacing = 10
for i,label in enumerate(ax.get_xticklabels()):
    if np.mod(i,tick_spacing)!=0:
        label.set_visible(False)

plt.title("Moody's corporate default rates, 1920-"+str(max(yearrange)))
plt.show()
