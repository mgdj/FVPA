from kubernetes import client, config

def is_pod_in_transition(podname):
    # 加载默认的Kubernetes配置文件
    config.load_kube_config()

    # 创建 Kubernetes API 客户端
    api = client.AppsV1Api()

    # 检查Pod是否属于迁移状态
    pod = api.read_namespaced_pod(podname, namespace="default")
    if pod.status.phase != "Running":
        return True

    # 检查Pod所属的Deployment或StatefulSet是否正在滚动升级
    owner_references = pod.metadata.owner_references
    if owner_references:
        owner = owner_references[0]
        if owner.kind == "Deployment":
            deployment = api.read_namespaced_deployment(owner.name, namespace="default")
            if deployment.status.updated_replicas < deployment.status.replicas:
                return True
        elif owner.kind == "StatefulSet":
            statefulset = api.read_namespaced_stateful_set(owner.name, namespace="default")
            if statefulset.status.updated_replicas < statefulset.status.replicas:
                return True

    return False
