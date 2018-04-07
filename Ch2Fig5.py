import matplotlib.pyplot as plt
tenors=[0.083333333,0.25,0.5,1,2,3,5,7,10,20,30]
#Curve source:
#https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield
curve20010102=[None,5.87,5.58,5.11,4.87,4.82,
               4.76,4.97,4.92,5.46,5.35]
                                        
plt.plot(tenors, curve20010102)
## Configure the graph
plt.title('US Treasury Curve 2001-01-02')
plt.ylim(0,7)
plt.xlabel('Tenor')
plt.ylabel('Rate')
plt.grid(True)
plt.show
