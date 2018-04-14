import matplotlib.pyplot as plt
import pandas as pd
from frmbook_funcs import GetFREDMatrix
from frmbook_funcs import TenorsFromNames
#Show the inverted Treasury curve from 2001-01-02

targetdate='2001-01-02'
#Note no one-month rate on this date
seriesnames=['DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
cdates,ratematrix=GetFREDMatrix(seriesnames,startdate=targetdate,enddate=targetdate)

plt.plot(TenorsFromNames(seriesnames), ratematrix[0])
## Configure the graph
plt.title('US Treasury Curve '+targetdate)
plt.ylim(0,max([x for x in ratematrix[0] if pd.notna(x)])+.5)
plt.xlabel('Tenor (years)')
plt.ylabel('Rate (%/year)')
plt.grid(True)
plt.show
