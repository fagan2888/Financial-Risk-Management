import matplotlib.pyplot as plt
import pandas as pd
#Show the inverted Treasury curve from
#2001-01-02

targetdate='2001-01-02'
#Note no one-month rate on this date
seriesnames=['DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
#GetFREDMatrix is in frmbook_funcs
cdates,ratematrix=GetFREDMatrix(seriesnames,startdate=targetdate,enddate=targetdate)

tenors=[0.25,0.5,1,2,3,5,7,10,20,30]

plt.plot(tenors, ratematrix[0])
## Configure the graph
plt.title('US Treasury Curve '+targetdate)
plt.ylim(0,max([x for x in ratematrix[0] if pd.notna(x)])+.5)
plt.xlabel('Tenor (years)')
plt.ylabel('Rate (%/year)')
plt.grid(True)
plt.show
