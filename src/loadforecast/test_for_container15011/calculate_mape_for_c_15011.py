import pandas as pd
import sys
sys.path.append(r'C:\Users\Administrator\Desktop\bscode\loadforecast')
from calculate_mape import calculate_mape
df_conf = pd.read_csv("../data/c_15011_confirm.csv",usecols=['yhat'])
df_fore = pd.read_csv("../data/c_15011_CPU_forecast_middle.csv",usecols=['yhat'])
mape = calculate_mape(df_conf,df_fore)
print(mape)