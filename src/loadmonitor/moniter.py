from prometheus_api_client import PrometheusConnect
import csv
import datetime

def collect_metrics_and_save_to_csv(prometheus_query, start_time, end_time, time_interval, output_file_path):
    """
    Collects metrics from Prometheus and saves them to a CSV file.

    Args:
        prometheus_query (str): Prometheus query to collect metrics.
        start_time (str): Start time in the format "YYYY-MM-DDTHH:MM:SSZ".
        end_time (str): End time in the format "YYYY-MM-DDTHH:MM:SSZ".
        time_interval (str): Time interval for collecting metrics, in the format "Xm".
        output_file_path (str): File path to save the collected metrics.

    Returns:
        None
    """
    # Create a Prometheus client object
    prometheus_client = PrometheusConnect(url="10.10.103.166:31979",headers=None,disable_ssl=True)
    #ok = prometheus_client.check_prometheus_connection()  # 检查连接状态
    ok = True
    if(ok):
        print("connection succesfully!")
    else:
        print("connection failed!")
    all_metrics = prometheus_client.all_metrics()
    print("------所有指标------")
    for metrics in all_metrics:
        print(metrics)
    print('------------------')
    # Collect metrics
    metrics = prometheus_client.get_metric_range_data(
        query=prometheus_query,
        start_time=start_time,
        end_time=end_time,
        step=time_interval
    )
    print("get data success")
    # Write metrics to CSV file
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ds', 'CPU_util', 'MEM_util'])
        for metric in metrics:
            timestamp = datetime.datetime.fromtimestamp(metric['time']).strftime('%Y-%m-%d %H:%M:%S')
            cpu_utilization = float(metric['values'][1])
            memory_utilization = float(metric['values'][0])
            writer.writerow([timestamp, cpu_utilization, memory_utilization])
    print("write success")