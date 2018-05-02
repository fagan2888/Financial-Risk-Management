import frmbook_funcs

#Get Fama-French market data. Convert to log-returns
Date,market_minus_rf,SMB,HML,RF=frmbook_funcs.getFamaFrench3()
ActualReality=frmbook_funcs.LogReturnConvert(market_minus_rf,RF)

#Generate sample standard deviations
lookbacks=[12,36,60]
SampleSd=frmbook_funcs.GenSampleSd(ActualReality,lookbacks)

#Graph
colors=['y-','b-','r-']
tstr='Figure 2, Sample US Stock Mkt σ, '
tstr+=str(Date[0])[:4]
tstr+='-'+str(Date[len(Date)-1])[:4]
frmbook_funcs.PlotSampleSd(tstr,Date,SampleSd,lookbacks,colors)
