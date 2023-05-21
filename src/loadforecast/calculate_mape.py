import numpy as np
import pandas as pd
def calculate_mape(col1, col2):
    '''
    计算两列数据的MAPE

    参数：
    col1: 第一列数据，类型为list
    col2: 第二列数据，类型为list

    返回值：
    两列数据的MAPE，类型为float
    '''
    if len(col1['yhat']) != len(col2['yhat']):
        raise ValueError('两列数据长度不一致')
    n = len(col1['yhat'])
    col1['yhat'] = col1['yhat'].astype(float)
    col2['yhat'] = col2['yhat'].astype(float)

    max_val = max(max(col1['yhat']), max(col2['yhat']))
    min_val = min(min(col1['yhat']), min(col2['yhat']))
    print(max_val)
    print(min_val)
    if max_val == min_val:
        raise ValueError('两列数据取值范围相同')
    norm_col1 = [x for x in col1['yhat']]
    norm_col2 = [x for x in col2['yhat']]
    mape = sum([abs(norm_col1[i]-norm_col2[i])/((norm_col1[i]+norm_col2[i])/2) for i in range(n)]) / n 
    return mape