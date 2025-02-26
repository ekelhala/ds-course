from kubernetes import client

def create_pod(kubernetes_client, definition):
    try:
        response = kubernetes_client.create_namespaced_pod("default", definition)
        return True
    except client.exceptions.ApiException:
        return False

def make_du_manifest(core_ip: str, core_port: int):
    """
    Creates a YAML manifest to start up a new DU
    based on given parameters
    """
    return {
        
    }
