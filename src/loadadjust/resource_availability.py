from kubernetes import client, config
from kubernetes.client.rest import ApiException


def check_resource_availability(pod_name, cpu_request, cpu_limit, mem_request, mem_limit):
    """
    Check if there are enough resources available on the Kubernetes cluster to assign to a pod
    with the given CPU and memory requests and limits.

    Args:
    - pod_name: str, the name of the pod.
    - cpu_request: float, the CPU request in millicores.
    - cpu_limit: float, the CPU limit in millicores.
    - mem_request: str, the memory request in bytes (e.g. '256Mi').
    - mem_limit: str, the memory limit in bytes (e.g. '1Gi').

    Returns:
    - bool, True if there are enough resources available; False otherwise.
    """

    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api = client.CoreV1Api()

    # Get the pod's namespace
    try:
        pod = api.read_namespaced_pod(name=pod_name, namespace='default')
        namespace = pod.metadata.namespace
    except ApiException as e:
        print("Exception when calling CoreV1Api->read_namespaced_pod")
        return False

    # Get the node list and available resources on each node
    try:
        nodes = api.list_node().items
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_node")
        return False

    for node in nodes:
        node_name = node.metadata.name
        node_cpus = int(node.status.allocatable['cpu'])
        node_mem = int(node.status.allocatable['memory'])
        node_cpu_request = 0
        node_cpu_limit = 0
        node_mem_request = 0
        node_mem_limit = 0

        # Get the current resource usage of all containers in all pods on the current node
        try:
            pods = api.list_namespaced_pod(namespace=namespace, field_selector="spec.nodeName={node_name}").items
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod")
            return False

        for pod in pods:
            for container in pod.spec.containers:
                # Get the CPU and memory request and limit of the container
                cpu_request = container.resources.requests.get('cpu')
                cpu_limit = container.resources.limits.get('cpu')
                mem_request = container.resources.requests.get('memory')
                mem_limit = container.resources.limits.get('memory')

                # Add the CPU and memory requests and limits of all containers on the current node
                node_cpu_request += int(cpu_request[:-1]) if cpu_request is not None else 0
                node_cpu_limit += int(cpu_limit[:-1]) if cpu_limit is not None else 0
                node_mem_request += int(mem_request[:-2]) if mem_request is not None else 0
                node_mem_limit += int(mem_limit[:-2]) if mem_limit is not None else 0

        # Check if there are enough resources available on the current node
        if node_cpus - node_cpu_request - node_cpu_limit >= cpu_request + cpu_limit and \
           node_mem - node_mem_request - node_mem_limit >= int(mem_request[:-2]) + int(mem_limit[:-2]):
            return True

    return False
