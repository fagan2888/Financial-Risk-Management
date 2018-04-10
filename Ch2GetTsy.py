#Get US Treasury constant maturity curve from FRED
#See http://mortada.net/python-api-for-fred.html
#for information on how to get the FRED (Federal
#Reserve of St. Louis database) API, and how to get
#an API key. The key below is Ken Winston's.
from fredapi import *
fred = Fred(api_key='fd97b1fdb076ff1a86aff9b38d7a0e70')
#Construct Fred series names
month=1./12.
tenors=[month,3*month,6*month,1,2,3,5,7,10,20,30]
seriesnames=['1MO','3MO','6MO','1','2','3','5','7','10','20','30']
for i,sn in enumerate(seriesnames):
    seriesnames[i]='DGS'+sn
#Get the time series for each tenor
#Put them all together in a dataframe
initialize=True
for sn in seriesnames:
    print('Processing ',sn)
    fs=fred.get_series(sn)
    fs=fs.rename(sn)   #put the name on the column
    if initialize:
        #Set up the dataframe with the first series
        dfcurve=pd.DataFrame(fs)
        initialize=False
    else:
        #concatenate the next series to the dataframe
        dfcurve=pd.concat([dfcurve,fs],axis=1)
        
