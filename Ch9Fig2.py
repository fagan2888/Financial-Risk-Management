#Show profitability graphs for Siegel's paradox -
#Philippe-Ken Wine Company

dollars_per_euro=1.17
x=np.arange(.34,2.01,.01)
z=x/dollars_per_euro
y_hedged=z+z**(-2)
y_unhedged=20*(1.1*z-1)

i=np.arange(len(x))
plt.plot(i,y_hedged,color='red',label='US/France')
plt.plot(i,y_unhedged,color='blue',label='France only')
plt.xticks(i[::20],x[::20])
plt.xlabel("Dollars per Euro")
plt.ylabel("Millions of Euros")
plt.legend(loc='lower right')
plt.title("Philippe-Ken Wine Company Profit")
plt.grid()
plt.show()

#zoomed-in graph
golden=(np.sqrt(5)+1)/2
x=np.arange(1,golden*dollars_per_euro*1.1,.01)
z=x/1.17
y_hedged=z+z**(-2)
y_constant=[2]*len(y_hedged)

i=np.arange(len(x))
plt.plot(i,y_hedged,color='red',label='US/France')
plt.plot(i,y_constant,color='green',label='Unchanged rates')
plt.xticks(i[::20],x[::20])
plt.xlabel("Dollars per Euro")
plt.ylabel("Millions of Euros")
plt.legend(loc='upper right')
plt.title("Philippe-Ken Wine Company Profit - neighborhood")
plt.grid()
plt.show()
