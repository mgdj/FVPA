import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from statsmodels.tsa.exponential_smoothing.ets import ETSModel
plt.rcParams["figure.figsize"] = (12, 8)

name = "bitcoin-price-usd"
input_csv_file_name = "C:/Users/Administrator/Desktop/bscode/data/MEM_util.csv"

data_df = pd.read_csv(input_csv_file_name)
# print(data_df.head())
print(type(data_df))
print(data_df)

# 1、先将index转成datetimeindex格式
index = pd.DatetimeIndex(data_df.iloc[:,0])
print(type(index))
print(index)
# 2、然后将数据先转成list
data_lst = data_df.iloc[:,1].tolist()
# 3、最后再用data_lst和index构建出新的series
data_series = pd.Series(data_lst, index=index)
data_series = data_series[:].astype("float64")
print(type(data_series))
print(data_series)

data_series.plot()
plt.ylabel("CPU")
plt.show()


train_data_series = data_series["2023-05-14 10:09:00":"2023-05-14 18:09:00"]
# train_data_series = data_series[:"2023-04-01T00:00:00.000Z"]

# fit in statsmodels
model = ETSModel(
    train_data_series,
    error="add",
    trend="add",
    seasonal="add",
    damped_trend=True,
    seasonal_periods=240,
)
# model = ETSModel(data_series)
fit = model.fit()
print(fit.fittedvalues)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# data_series.plot(label="data")
train_data_series.plot(label="data")
plt.ylabel("bitcoin price")

fit.fittedvalues.plot(label="statsmodels fit")
plt.legend()
plt.show()

print(fit.summary())


# prediction
pred = fit.get_prediction(start="2023-05-14 18:09:00", end="2023-05-14 20:09:00")
df = pred.summary_frame(alpha=0.4)  # 表示置信区间为95%
print(df)

# pred.endog.plot(label="data")
data_series.plot(label="data")

simulated = fit.simulate(anchor="end", nsimulations=30, repetitions=100)
for i in range(simulated.shape[1]):
    simulated.iloc[:, i].plot(label="_", color="gray", alpha=0.1)

df["mean"].plot(label="mean prediction")
df["pi_lower"].plot(linestyle="--", color="tab:blue", label="95% interval")
df["pi_upper"].plot(linestyle="--", color="tab:blue", label="_")

print(df)
df.to_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_fore.csv")

plt.legend()
plt.show()




