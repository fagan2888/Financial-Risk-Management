import frmbook_funcs

#Get Fama-French market data. Convert to log-returns
Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

#Generate sample standard deviations
lookbacks=[12,36,30]
SampleSd=GenSampleSd(ActualReality,lookbacks)

#Graph
colors=['y-','b-','r-']
frmbook_funcs.PlotSampleSd('Figure 2',Date,SampleSd,lookbacks,colors)
