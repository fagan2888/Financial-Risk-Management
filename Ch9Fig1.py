#Show numbr-of-bottles curve for Siegel's paradox

dollars_per_euro=1.17
x=np.arange(dollars_per_euro-.3,dollars_per_euro+.3+.01,.01)
z=x/dollars_per_euro
y=z+1/z

i=np.arange(len(x))
plt.plot(i,y,color='red')
plt.xticks(i[::10],x[::10])
plt.xlabel("Dollars per Euro")
plt.ylabel("Millions of bottles")
plt.title("Total bottle volume of Philippe-Ken Wine Company")
plt.grid()
plt.show()
