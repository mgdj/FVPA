import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import make_interp_spline

df=pd.read_csv("mysql_late.csv")

# 1、先将index转成datetimeindex格式
index = pd.DatetimeIndex(df.iloc[:,0])
print(type(index))
print(index)
# 2、然后将数据先转成list
data_1st = df.iloc[:,1].tolist()
data_2st = df.iloc[:,2].tolist()
# 3、最后再用data_lst和index构建出新的series
data_series1 = pd.Series(data_1st, index=index)
data_series2 = pd.Series(data_2st, index=index)
data_series1 = data_series1[:].astype("float64")
data_series2 = data_series2[:].astype("float64")
print(type(data_series1))
print(data_series1)

timeindex = pd.date_range(start="2023-05-14 20:20:00",end="2023-05-14 20:50:00",freq="10s")
print(type(timeindex))
data1_smooth = make_interp_spline(index,data_series1)(timeindex)

data2_smooth = make_interp_spline(index,data_series2)(timeindex)

plt.plot(timeindex,data1_smooth)
plt.plot(timeindex,data2_smooth)


ax = plt.gca()
# 设置日期的显示格式
date_format = mpl.dates.DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(date_format)


plt.ylabel("mysql latency/ms")
plt.legend(['latency for vpa','latency for my system'])
plt.show()
