import matplotlib.pyplot as plt
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
from frmbook_funcs import GetTenorNames
from frmbook_funcs import InterpolateCurve
#Get a yearend US Treasury curve
#Interpolate it to monthly and compute a short
#rate curve based on that
#Plot both

lastday=LastYearEnd()
seriesnames=['DGS1MO','DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
cdates,ratematrix=GetFREDMatrix(seriesnames,startdate=lastday,enddate=lastday)
tenorsfromtsy=GetTenorNames(seriesnames)

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
