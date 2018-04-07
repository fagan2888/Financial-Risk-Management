import matplotlib.pyplot as plt
#Plot first 3 principal components from Table 2 in
#https://pdfs.semanticscholar.org/c0ca/bab4aebf9d04e58a3084e4f35ea4d57045aa.pdf
tenornames=['3mo','6mo','1yr','2yr','3yr',
        '4yr','5yr','7yr','10yr','30yr']
tenornumbers=range(len(tenornames))
pc1=[0.21,0.26,0.32,0.35,0.36,
     0.36,0.36,0.34,0.31,0.25]
pc2=[-0.57,-0.49,-0.32,-0.1,0.02,
     0.14,0.17,0.27,0.3,0.33]
pc3=[0.5,0.23,-0.37,-0.38,-0.3,
     -0.12,-0.04,0.15,0.23,0.46]
plt.plot(tenornumbers, pc1, label='PC1')
plt.plot(tenornumbers, pc2, label='PC2')
plt.plot(tenornumbers, pc3, label='PC3')

## Configure the graph
plt.title('UST Curve Principal Components')
plt.xlabel('Tenor')
plt.ylabel('Level')
plt.legend()
plt.xticks(tenornumbers, tenornames)
plt.grid(True)
plt.show
