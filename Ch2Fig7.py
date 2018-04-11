import matplotlib.pyplot as plt
import pandas as pd
#Get a yearend US Treasury curve
#Interpolate it to monthly and compute a short
#rate curve based on that
#Plot both

tenorsfromtsy,seriesnames,cdates,ratematrix=GetUSCurve()
#find end of last year
t=pd.Timestamp.now()
for day in [31,30,29,28]:
    lastday=str(t.year-1)+'-12-'+str(day)
    if lastday in cdates:
       break

#Get monhtly interpolated curve and short rate curve
curvefromtsy=ratematrix[cdates.index(lastday)]
tenors,curvemonthly,shortrates=InterpolateCurve(tenorsfromtsy,curvefromtsy)

plt.plot(tenors, curvemonthly, label=lastday)
plt.plot(tenors, shortrates, label='Short')
## Configure the graph
plt.title('US Treasury and Short Rate Curve')
plt.xlabel('Rate')
plt.ylabel('Tenor')
plt.ylim(0,max(curvemonthly)+.5)
plt.legend()
plt.grid(True)
plt.show
