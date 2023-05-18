from kubernetes import client, config

# 加载 Kubernetes 配置文件
config.load_kube_config()

def check_pod_writing_file(podname):
    v1 = client.CoreV1Api()
    logs = v1.read_namespaced_pod_log(name=podname, namespace='default')
    # 判断日志信息中是否有正在写入文件的标志，可以根据实际情况自定义
    if 'writing file' in logs:
        return True
    else:
        return False
