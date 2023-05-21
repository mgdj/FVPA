import sys

sys.path.append(r'C:\Users\Administrator\Desktop\bscode\admissioncontroller')
sys.path.append(r'C:\Users\Administrator\Desktop\bscode\loadforecast')
sys.path.append(r'C:\Users\Administrator\Desktop\bscode\loadmonitor')

#from loadmonitor.moniter import collect_metrics_and_save_to_csv
from loadforecast.forecast import forecast

#from loadadjust.expansion_contraction import load_expansion_contraction
def controller():
    #获取测试数据
    '''prometheus_query = 'rate(container_cpu_user_seconds_total{container_label_io_kubernetes_container_name="mysql",container_label_io_kubernetes_pod_name="mysql-0"}[5m])'
    start_time = '2023-05-14T02:00:00Z'
    end_time = '2023-05-14T6:59:59Z'
    time_interval = '1m'
    output_file_path1 = '..\data\CPU_MEM.csv'

    collect_metrics_and_save_to_csv(prometheus_query, start_time, end_time, time_interval, output_file_path1)'''
    
    #此部分主要用于测试以获取验证数据，查看预测正确率
    #prometheus_query = 'sum(rate(container_cpu_usage_seconds_total{pod_name="mysql-0"}[5m])) / count(container_memory_usage_bytes{pod_name="mysql-0"})'
    #start_time = '2023-05-08T00:00:00Z'
    #end_time = '2023-05-08T23:59:59Z'
    #time_interval = '10m'
    #output_file_path2 = '..\data\confirm.csv'
    #collect_metrics_and_save_to_csv(prometheus_query, start_time, end_time, time_interval, output_file_path2)
    
    output_file_path_CPU = '..\data\CPU_Request_Limit.csv'
    output_file_path_MEM = '..\data\MEM_Request_Limit.csv'
    forecast(output_file_path_CPU,output_file_path_MEM)

    '''podname = 'mysql-0'
    load_expansion_contraction(podname)'''
    