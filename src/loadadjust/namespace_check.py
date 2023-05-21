from kubernetes import client, config

def check_pod_resources(pod_name, cpu_request, cpu_limit, mem_request, mem_limit, namespace):
    # 加载 Kubernetes 配置文件
    config.load_kube_config()

    # 创建 Kubernetes 的 API 客户端
    api = client.CoreV1Api()

    # 获取指定 Namespace 的资源使用情况
    namespace_info = api.read_namespace(namespace)
    namespace_cpu_used = namespace_info.status.allocatable["cpu"] - namespace_info.status.capacity["cpu"]
    namespace_mem_used = namespace_info.status.allocatable["memory"] - namespace_info.status.capacity["memory"]

    # 获取 Pod 的 CPU 和内存资源请求和限制
    pod_info = api.read_namespaced_pod(pod_name, namespace)
    pod_cpu_request = pod_info.spec.containers[0].resources.requests["cpu"]
    pod_cpu_limit = pod_info.spec.containers[0].resources.limits["cpu"]
    pod_mem_request = pod_info.spec.containers[0].resources.requests["memory"]
    pod_mem_limit = pod_info.spec.containers[0].resources.limits["memory"]

    # 计算 Pod 请求的资源量
    pod_cpu_amount = (cpu_request + cpu_limit) * 1000  # 转换为毫核
    pod_mem_amount = mem_request + mem_limit  # 单位为字节

    # 检查资源是否足够
    if pod_cpu_amount > (namespace_info.status.allocatable["cpu"] - namespace_cpu_used):
        print("Error: Insufficient CPU resources in Namespace.")
        return False
    if pod_mem_amount > (namespace_info.status.allocatable["memory"] - namespace_mem_used):
        print("Error: Insufficient Memory resources in Namespace.")
        return False

    # 资源充足，可以进行资源分配
    # 设置 Pod 的 CPU 和内存资源请求和限制
    pod_info.spec.containers[0].resources.requests["cpu"] = str(cpu_request) + "m"
    pod_info.spec.containers[0].resources.limits["cpu"] = str(cpu_limit) + "m"
    pod_info.spec.containers[0].resources.requests["memory"] = str(mem_request) + "Mi"
    pod_info.spec.containers[0].resources.limits["memory"] = str(mem_limit) + "Mi"
    api.patch_namespaced_pod(pod_name, namespace, pod_info)
    return True
