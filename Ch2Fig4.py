import matplotlib.pyplot as plt
import pandas as pd
from frmbook_funcs import GetFREDMatrix
from frmbook_funcs import LastYearEnd
from frmbook_funds import TenorsFromNames
#Plot the 2010, 2012, and most recent yearend
#US Treasury curves
seriesnames=['DGS1MO','DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
cdates,ratematrix=GetFREDMatrix(seriesnames)

#Form the list of curve dates to display
displaydates=['2010-12-31','2012-12-31']
displaydates.append(LastYearEnd())
tenors=TenorsFromNames(seriesnames)

#Plot the three lines
for i in range(3):
    year=displaydates[i][:4]
    plt.plot(tenors,
        ratematrix[cdates.index(displaydates[i])],
        label=year)

## Configure the graph
plt.title('US Yearend Treasury Curves')
plt.xlabel('Tenor (years)')
plt.ylabel('Rate (%/year)')
plt.legend()
plt.grid(True)
plt.annotate('Upward sloping', xy=(25, 2.5), xytext=(21.25, 0),
            arrowprops=dict(arrowstyle='<->',
                    facecolor='black'))
plt.text(.5, 1, 'Short end')
plt.text(15, 3, 'Belly')
plt.text(25, 4, 'Long end')
plt.show
