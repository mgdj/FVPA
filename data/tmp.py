import pandas as pd
from fbprophet import Prophet

df = pd.read_csv("CPU_real.csv")

df_MEM = pd.read_csv("MEM_real.csv")

df['MEM'] = df_MEM['MEM']

df['MEM'] = df['MEM'].astype(float)
df['CPU'] = df['CPU'].astype(float)

df['MEM'] = [x/1000 for x in df['MEM']]
df['CPU'] = [x*2000 for x in df['CPU']]

df.to_csv("CPU_MEM.csv",index = False)