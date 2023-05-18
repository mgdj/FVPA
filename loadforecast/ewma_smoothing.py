import pandas as pd

def ewma_smoothing(file_path, alpha=0.1):
    # 读取CSV文件
    df = pd.read_csv(file_path, usecols=['ds', 'CPU', 'MEM'])
    # 将时间戳设置为索引
    df.set_index('ds', inplace=True)
    # 使用指数加权移动平均值进行平滑处理
    df['smoothed_CPU'] = df['CPU'].ewm(alpha=alpha).mean()

    df['smoothed_MEM'] = df['MEM'].ewm(alpha=alpha).mean()

    df.to_csv(file_path)

    print("EWMA_smoothing successfully！")
    return True