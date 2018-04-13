import matplotlib.pyplot as plt
import pandas as pd
#Get a yearend US Treasury curve
#Interpolate it to monthly and compute a short
#rate curve based on that
#Plot both

#find end of last year
t=pd.Timestamp.now()
for day in [31,30,29,28]:
    lastday=str(t.year-1)+'-12-'+str(day)
    if pd.Timestamp(lastday).weekday()<5:
       break

seriesnames=['DGS1MO','DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
#GetFREDMatrix is in frmbook_funcs
cdates,ratematrix=GetFREDMatrix(seriesnames,startdate=lastday,enddate=lastday)

#Extract numerical (yearly) tenors from series names
tenorsfromtsy=[]
for i in range(len(seriesnames)):
    if seriesnames[i][-2:]=='MO':
        tenorsfromtsy.append(float(seriesnames[i][3:-2])/12)
    else:
        tenorsfromtsy.append(float(seriesnames[i][3:]))

#Get monhtly interpolated curve and short rate curve
#InterpolateCurve is in frmbook_funcs
tenors,curvemonthly,shortrates=InterpolateCurve(tenorsfromtsy,ratematrix[0])

plt.plot(tenors, curvemonthly, label=lastday)
plt.plot(tenors, shortrates, label='Short')
## Configure the graph
plt.title('US Treasury and Short Rate Curves')
plt.xlabel('Tenor (years)')
plt.ylabel('Rate (%/year)')
plt.ylim(0,max(curvemonthly)+.5)
plt.legend()
plt.grid(True)
plt.show
