import matplotlib.pyplot as plt
#Show the inverted Treasury curve from
#2001-01-02

targetdate='2001-01-02'
tenorsfromtsy,seriesnames,cdates,ratematrix=GetUSCurve()
curvetarget=ratematrix[cdates.index(targetdate)]
                                        
plt.plot(tenorsfromtsy, curvetarget)
## Configure the graph
plt.title('US Treasury Curve '+targetdate)
plt.ylim(0,max([x for x in curvetarget if pd.notna(x)])+.5)
plt.xlabel('Tenor')
plt.ylabel('Rate')
plt.grid(True)
plt.show
