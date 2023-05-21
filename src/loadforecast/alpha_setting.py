import pandas as pd

#获取CPU利用率最佳alpha值
def get_CPU_alpha():

    df_up = pd.read_csv("..\data\\forecast_CPU_24h_up.csv")
    df_low = pd.read_csv("..\data\\forecast_CPU_24h_low.csv")
    df_middle = pd.read_csv("..\data\\forecast_CPU_24h_middle.csv")
    df_confirm = pd.read_csv("..\data\\confirm_CPU_util.csv")

    alp = 0.1
    temp = float('inf')
    temp_alp = alp
    while alp <= 0.5:
        i = 2
        sum = (df_up[1][1] - df_confirm[1][1]) * (df_up[1][1] - df_confirm[1][1])
        while i <= 144:
            sum+=(df_up[i][1] * (1 - alp) + df_up[i-1][1] * alp - df_confirm[i][1]) * (df_up[i][1] * (1 - alp) + df_up[i-1][1] * alp - df_confirm[i][1])
            i+=1
        if sum <= temp:
            temp = sum
            temp_alp = alp
        alp += 0.1
    return temp_alp

#获取内存利用率最佳alpha值
def get_MEM_alpha():
    df_up = pd.read_csv("..\data\\forecast_MEM_24h_up.csv")
    df_low = pd.read_csv("..\data\\forecast_MEM_24h_low.csv")
    df_middle = pd.read_csv("..\data\\forecast_MEM_24h_middle.csv")
    df_confirm = pd.read_csv("..\data\\confirm_MEM_util.csv")

    alp = 0.1
    temp = float('inf')
    temp_alp = alp
    while alp <= 0.5:
        i = 2
        sum = (df_up[1][1] - df_confirm[1][1]) * (df_up[1][1] - df_confirm[1][1])
        while i <= 144:
            sum+=(df_up[i][1] * (1 - alp) + df_up[i-1][1] * alp - df_confirm[i][1]) * (df_up[i][1] * (1 - alp) + df_up[i-1][1] * alp - df_confirm[i][1])
            i+=1
        if sum <= temp:
            temp = sum
            temp_alp = alp
        alp += 0.1
    return temp_alp