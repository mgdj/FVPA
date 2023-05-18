from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time

def update_pod_resources(pod_name, cpu_req, cpu_limit, mem_req, mem_limit):
    # 加载 Kubernetes 配置
    config.load_kube_config(config_file='/root/.kube/config')
    
    # 创建 Kubernetes API 的 CoreV1Api 实例
    api = client.CoreV1Api()
    
    try:
        # 获取 Pod 的信息
        pod = api.read_namespaced_pod(pod_name, "default")
        
        # 获取 Pod 所在的 Node 名称
        node_name = pod.spec.node_name
        
        # 获取 Pod 所在的 Namespace
        namespace = pod.metadata.namespace
        
        # 获取 Pod 中 container 的 Request 和 Limit 信息
        container = pod.spec.containers[0]
        cpu_request = container.resources.requests.get('cpu')
        cpu_limit_current = container.resources.limits.get('cpu')
        mem_request = container.resources.requests.get('memory')
        mem_limit_current = container.resources.limits.get('memory')

        # 计算新的 Request 和 Limit 的值
        new_cpu_limit = str(cpu_limit)
        new_cpu_request = str(cpu_req)
        new_mem_limit = str(mem_limit)
        new_mem_request = str(mem_req)

        # 构造 Patch 请求的 body
        patch_body = {
            "spec": {
                "containers": [
                    {
                        "name": container.name,
                        "resources": {
                            "requests": {
                                "cpu": new_cpu_request,
                                "memory": new_mem_request
                            },
                            "limits": {
                                "cpu": new_cpu_limit,
                                "memory": new_mem_limit
                            }
                        }
                    }
                ]
            }
        }

        # 更新 Pod 的资源配置
        api.patch_namespaced_pod(pod_name, namespace, patch_body)

        # 等待 Pod 更新完成
        updated = False
        while not updated:
            # 获取更新后的 Pod 的信息
            pod = api.read_namespaced_pod(pod_name, namespace)

            # 判断 Pod 是否更新完成
            if pod.status.phase == "Running" and pod.status.container_statuses[0].ready:
                updated = True

            # 等待一段时间后再次检查
            time.sleep(2)

    except ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_pod: %s\n" % e)

    return updated
