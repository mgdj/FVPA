import pandas as pd
import csv
import datetime
#from fbprophet import Prophet
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_pacf,plot_acf
import matplotlib.pyplot as plt
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from alpha_setting import get_CPU_alpha
from alpha_setting import get_MEM_alpha
from ewma_smoothing import ewma_smoothing
from calculate_mape import calculate_mape

def forecast(output_file_path_CPU,output_file_path_MEM):
    ewma_smoothing("C:/Users/Administrator/Desktop/bscode/data/CPU_MEM.csv")
    f_CPU = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_MEM.csv",usecols=['ds','smoothed_CPU'])
    f_CPU.columns = ['ds','y']
    f_CPU.to_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_util.csv",index=False)    
    f_MEM = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_MEM.csv",usecols=['ds','smoothed_MEM'])
    f_MEM.columns = ['ds','y']
    f_MEM.to_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_util.csv",index=False)

    '''f_CPU_confirm = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/confirm.csv",usecols=['ds','CPU_util'])
    f_CPU_confirm.to_csv("C:/Users/Administrator/Desktop/bscode/data/confirm_CPU_util.csv") 
    f_MEM_confirm = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/confirm.csv",usecols=['ds','MEM_util'])
    f_MEM_confirm.to_csv("C:/Users/Administrator/Desktop/bscode/data/confirm_MEM_util.csv") '''

    df = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_util.csv")
    df.columns = ['ds','y']
    df.to_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_util.csv",index=False)
    
    df = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_util.csv")
    df.columns = ['ds','y']
    df.to_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_util.csv",index=False)

    df_CPU = pd.read_csv('C:/Users/Administrator/Desktop/bscode/data/CPU_util.csv')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(1)
    print(df_CPU.head())

    df_data = df_CPU['y']
    print(df_data)
    oil = pd.Series(df_CPU['y'],index = pd.date_range("2023-5-14 10:09:00","2023-5-14 18:09:00",freq="1m"))
    print(oil.size)
    oil.plot()
    #df_CPU.set_index('ds')

    # 1、先将index转成datetimeindex格式
    '''index = pd.DatetimeIndex(df_CPU.iloc[:,0])
    # print(type(index))
    # print(index)
    # 2、然后将数据先转成list
    data_lst = df_CPU.iloc[:,1].tolist()
    # 3、最后再用data_lst和index构建出新的series
    data_series = pd.Series(data_lst, index=index)
    data_series = data_series[:].astype("float64")
    # print(type(data_series))
    # print(data_series)

    df_CPU = data_series

    print(df_CPU)
    df_CPU.plot()
    plt.show()
    #plt.plot(df_CPU.index,df_CPU['y'].values)
    #plt.show()
    #df_CPU= df_CPU['y'].diff(1)
    print(df_CPU)
    acf = plot_acf(df_CPU)
    plt.title("总有功功率的自相关图")
    plt.show()

    pacf=plot_pacf(df_CPU)
    plt.title("总有功功率的偏自相关图")
    plt.show()
    model = sm.tsa.arima.ARIMA(df_CPU,order=(50,0,1))
    arima_res=model.fit()
    arima_res.summary()

    predict=arima_res.predict("2023-5-14 18:09:00","2023-5-14 20:09:00")
    print(type(predict))
    print(predict)
    # df_CPU=df_CPU["2023-5-13 10:09:00":"2023-5-14 10:09:00"]
    # plt.plot(df_CPU.index,df_CPU['y'])
    # plt.plot(df_CPU.index,predict)
    # plt.legend(['y_true','y_pred'])
    plt.plot(df_CPU, label='y_true')
    plt.plot(predict, label='y_pred')
    plt.show()
    print(len(predict))'''
    '''df_CPU['cap'] = 8.5
    m_CPU = Prophet(changepoint_range=1,changepoint_prior_scale=0.5,growth='logistic')
    m_CPU.fit(df_CPU)

    future_CPU = m_CPU.make_future_dataframe(freq='1min',periods=20)
    future_CPU.tail()

    forecast_CPU = m_CPU.predict(future_CPU)

    forecast_CPU_24h = forecast_CPU.iloc[-20:]

    #此部分主要用于验证预测准确性
    #forecast_CPU_24h_test = forecast_CPU_24h['yhat']
    #df_CPU_test = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/confirm.csv", usecols=['CPU_util'])
    #mape_CPU = calculate_mape(forecast_CPU_24h_test,df_CPU_test)
    #print(mape_CPU)

    forecast_CPU_24h_middle = forecast_CPU_24h[['ds', 'yhat']]
    forecast_CPU_24h_middle.to_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_forecast_middle.csv",index=False)

    forecast_CPU_24h_up = forecast_CPU_24h[['ds', 'yhat_upper']]
    forecast_CPU_24h_up.to_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_forecast_24h_up.csv",index=False)

    forecast_CPU_24h_low = forecast_CPU_24h[['ds', 'yhat_lower']]
    forecast_CPU_24h_low.to_csv("C:/Users/Administrator/Desktop/bscode/data/CPU_forecast_24h_low.csv",index=False)

    print(forecast_CPU_24h[['ds', 'yhat']])

    forecast_CPU[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    m_CPU.plot(forecast_CPU)

    m_CPU.plot_components(forecast_CPU)
    plt.show()'''

    df_MEM = pd.read_csv('C:/Users/Administrator/Desktop/bscode/data/MEM_util.csv')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(1)
    print(df_MEM.head())
    m_MEM = Prophet(changepoint_range=1,changepoint_prior_scale=0.5,)
    m_MEM.fit(df_MEM)

    future_MEM = m_MEM.make_future_dataframe(freq='1min',periods=20)
    future_MEM.tail()

    forecast_MEM = m_MEM.predict(future_MEM)

    forecast_MEM_24h = forecast_MEM.iloc[-20:]

    #此部分用于测试预测准确性
     #此部分主要用于验证预测准确性
    #forecast_MEM_24h_test = forecast_MEM_24h['yhat']
    #df_MEM_test = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/confirm.csv", usecols=['MEM_util'])
    #mape_MEM = calculate_mape(forecast_MEM_24h_test,df_MEM_test)
    #print(mape_MEM)

    forecast_MEM_24h_middle = forecast_MEM_24h[['ds', 'yhat']]
    forecast_MEM_24h_middle.to_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_forecast_middle.csv",index=False)

    forecast_MEM_24h_up = forecast_MEM_24h[['ds', 'yhat_upper']]
    forecast_MEM_24h_up.to_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_forecast_24h_up.csv",index=False)

    forecast_MEM_24h_low = forecast_MEM_24h[['ds', 'yhat_lower']]
    forecast_MEM_24h_low.to_csv("C:/Users/Administrator/Desktop/bscode/data/MEM_forecast_24h_low.csv",index=False)

    print(forecast_MEM_24h[['ds', 'yhat']])

    forecast_MEM[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    m_MEM.plot(forecast_MEM)

    m_MEM.plot_components(forecast_MEM)
    plt.show()

    CPU_alpha = get_CPU_alpha()

    MEM_alpha = get_MEM_alpha()

    df_up = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/forecast_CPU_24h_up.csv")
    df_low = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/forecast_CPU_24h_low.csv")
    df_middle = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/forecast_CPU_24h_middle.csv")
    with open(output_file_path_CPU, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ds', 'Request', 'Limit'])
        writer.writerow([df_up[1][0],df_middle[1][1],df_up[1][1]])
        i=2
        while i <= 144:
            timestamp = df_up[i][0]
            request = df_middle[i][1]
            limit = df_up[i][1]*0.9 + df_up[i-1][1]*0.1
            writer.writerow([timestamp, request, limit])
    df_up = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/forecast_MEM_24h_up.csv")
    df_low = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/forecast_MEM_24h_low.csv")
    df_middle = pd.read_csv("C:/Users/Administrator/Desktop/bscode/data/forecast_MEM_24h_middle.csv")
    with open(output_file_path_MEM, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ds', 'Request', 'Limit'])
        writer.writerow([df_up[1][0],df_middle[1][1],df_up[1][1]])
        i=2
        while i <= 144:
            timestamp = df_up[i][0]
            request = df_middle[i][1]
            limit = df_up[i][1]*0.9 + df_up[i-1][1]*0.1
            writer.writerow([timestamp, request, limit])