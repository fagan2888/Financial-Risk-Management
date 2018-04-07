import matplotlib.pyplot as plt
tenors=[0.083333333,0.25,0.5,1,2,3,5,7,10,20,30]
#Curve source:
#https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield
curve2010=[0.07,0.12,0.19,0.29,0.61,1.02,
           2.01,2.71,3.3,4.13,4.34]
curve2012=[0.02,0.05,0.11,0.16,0.25,0.36,
           0.72,1.18,1.78,2.54,2.95]
curve2017=[1.28,1.39,1.53,1.76,1.89,1.98,
           2.2,2.33,2.4,2.58,2.74]
                                             
plt.plot(tenors, curve2010, label='2010')
plt.plot(tenors, curve2012, label='2012')
plt.plot(tenors, curve2017, label='2017')
## Configure the graph
plt.title('US Treasury Curves')
plt.xlabel('Tenor')
plt.ylabel('Rate')
plt.legend()
plt.grid(True)
plt.annotate('Upward sloping', xy=(25, 2.5), xytext=(21.25, 0),
            arrowprops=dict(arrowstyle='<->',
                    facecolor='black'))
plt.text(.5, 1, 'Short end')
plt.text(15, 3, 'Belly')
plt.text(25, 4, 'Long end')
plt.show
