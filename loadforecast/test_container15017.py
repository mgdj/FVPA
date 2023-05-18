import csv
import pandas as pd
from fbprophet import Prophet 
from ewma_smoothing import ewma_smoothing
import matplotlib.pyplot as plt

ewma_smoothing("C:/Users/Administrator/Desktop/bscode/data/c_15017_CPU_util.csv")
f_CPU = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/c_15017_CPU_util.csv",usecols=['ds','smoothed_CPU'])
f_CPU.columns=['ds','y']
f_CPU.to_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_util.csv")    

df_CPU = pd.read_csv('C:/Users/Administrator/Desktop/bscode/data/CPU_util.csv')

print(df_CPU.head())
m_CPU = Prophet()
m_CPU.fit(df_CPU)

future_CPU = m_CPU.make_future_dataframe(freq='10min',periods=144)
future_CPU.tail()

forecast_CPU = m_CPU.predict(future_CPU)

forecast_CPU_24h = forecast_CPU.iloc[-144:]

forecast_CPU_24h_middle = forecast_CPU_24h[['ds', 'yhat']]
forecast_CPU_24h_middle.to_csv("C:/Users/Administrator/Desktop/bscode/data//c_15017_CPU_forecast_middle.csv",index=False)

forecast_CPU_24h_up = forecast_CPU_24h[['ds', 'yhat_upper']]
forecast_CPU_24h_up.to_csv("C:/Users/Administrator/Desktop/bscode/data//c_15017_CPU_forecast_24h_up.csv",index=False)

forecast_CPU_24h_low = forecast_CPU_24h[['ds', 'yhat_lower']]
forecast_CPU_24h_low.to_csv("C:/Users/Administrator/Desktop/bscode/data//c_15017_CPU_forecast_24h_low.csv",index=False)
forecast_CPU[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

m_CPU.plot(forecast_CPU)

m_CPU.plot_components(forecast_CPU)
plt.show()