import matplotlib.pyplot as plt
#Plot a short rate curve
tenornames=['1mo','3mo','6mo','1yr','2yr','3yr',
        '5yr','7yr','10yr','20yr','30yr']
tenornumbers=range(len(tenornames))
tenors=[0.083333333,0.25,0.5,1,2,3,5,7,10,20,30]
#Curve source:
#https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield
curve2017=[1.28,1.39,1.53,1.76,1.89,1.98,
           2.2,2.33,2.4,2.58,2.74]
curve=curve2017
yeartext='2017'
                                             
plt.plot(tenornumbers, curve, label=yeartext)
#Bootstrap a short rate curve

shortrates=[]
for i,rate in enumerate(curve):
    short=curve[i]    
    if (i!=0):
        denom=tenors[i]-tenors[i-1]
        numer=curve[i]-curve[i-1]
        if (denom!=0):
            short+=numer/denom
    shortrates.append(short)

plt.plot(tenornumbers, shortrates, label='Short')
## Configure the graph
plt.title('US Treasury and Short Rate Curve')
plt.xlabel('Rate')
plt.ylabel('Tenor')
plt.ylim(0,3)
plt.xticks(tenornumbers,tenornames)
plt.legend()
plt.grid(True)
plt.show
