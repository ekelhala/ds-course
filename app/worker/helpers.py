from kubernetes import client

def create_pod(kubernetes_client, definition):
    try:
        response = kubernetes_client.create_namespaced_pod("default", definition)
        return True
    except client.exceptions.ApiException:
        return False

def make_cu_configmap(core_ip: str, core_port: int):
    """
    Creates a ConfigMap to start up a new CU
    based on given parameters
    """
    cu_id = 0
    config_data = f"""
    log:
      filename: stdout
      cu_level: info

    cu_cp:
      amf:
        no_core: true
        addr: {core_ip}
        bind_addr: __MY_IP__
        supported_tracking_areas:
          - tac: 7
            plmn_list:
              - plmn: "00101"
                tai_slice_support_list:
                  - sst: 1
      f1ap:
        bind_addr: __MY_IP__

    expert_execution:
      threads:
        non_rt:
          nof_non_rt_threads: 2
    """
    return client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        metadata=client.V1ObjectMeta(
            name=f"cu-config-{cu_id}",
        ),
        data={"cu.yaml": config_data}
    )
