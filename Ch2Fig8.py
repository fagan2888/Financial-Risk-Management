import pandas as pd
import datetime
import requests
import re
import matplotlib.pyplot as plt
#Download and plot 10-year Swiss rates
#from the Swiss National Bank
#Kinda convoluted, sorry - complain to the Swiss!
# get current timestamp
dt = f"{datetime.datetime.utcnow():%Y%m%d_%H%M%S}"
# construct reference file id URL
refurl = "https://data.snb.ch/json/chart/getChartExcelFileRef?lang=EN&pageViewTime=%s" % dt
# Get file id for this chart 
x = requests.post(refurl, headers={"Content-type": "application/json;charset=UTF-8"}, data='{"chartId":"rendeidglfzch"}')
s = x.content.decode("UTF-8")
# Strip away the beginning and the end of the string, leaving the fileid
s = re.sub(r'^.*\n{"fileid":"', '', s)
s = re.sub(r'"}', '', s)
# Construct download URL
fileurl = 'https://data.snb.ch/json/table/getFile?fileId=%s&pageViewTime=%s&lang=en' % (s, dt)
# Read file directly.  Skip unnecessary rows at the top.
df = pd.read_excel(fileurl, skiprows=15)

#dataframe now contains dates and rates
#move to lists for plotting
dates=df['Unnamed: 0'].tolist()
rates=df["10 years"].tolist()
#find first date in 2014
start2014=6782   #As of 2018
string2014='2014-01-0'
for day in range(5):
    if (string2014+str(day)) in dates:
        start2014=dates.index(string2014+str(day))
        break

#Plot 10-year rate since the beginning of 2014
datenumbers=range(len(dates)-start2014)
plt.plot(datenumbers, rates[start2014:])
## Configure the graph
plt.title('Swiss 10-year rates')
plt.xlabel('Date')
plt.ylabel('Rate')
#only show dates every 90 days
datenumbers=range(0,len(dates)-start2014,90)
showdates=[dates[i] for i in range(start2014,len(dates),90)]
plt.xticks(datenumbers,showdates,rotation='vertical')
#Get minimum for shaded area below 0
minrate=round(min(rates[start2014:])-.5)
plt.fill_between(range(len(dates)-start2014), minrate, 0, facecolor='red', alpha=0.1)
plt.grid(True)
plt.show
