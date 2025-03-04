from kubernetes import client

def create_pod(kubernetes_client, definition):
    try:
        response = kubernetes_client.create_namespaced_pod("default", definition)
        return True
    except client.exceptions.ApiException:
        return False

def make_configmap(core_ip: str, core_port: int, config_id: str):
    """
    Creates a ConfigMap to start up a new CU
    based on given parameters
    """
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
            name=f"component-configs-{config_id}",
        ),
        data={"cu.yaml": config_data}
    )

def make_deployment_config(unique_id):
  try: 
    deployment = client.V1Deployment(
      api_version="apps/v1",
      kind="Deployment",
      metadata=client.V1ObjectMeta(
        name=f"srsran-{unique_id}"
      ),
      spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
              match_labels={"app": "srsran-cu", "unique-id": unique_id}
        ),
        template=client.V1PodTemplateSpec(
          metadata=client.V1ObjectMeta(
            labels={"app": "srsran-cu", "unique-id": unique_id}
          ),
          spec=client.V1PodSpec(
            init_containers=[
                      client.V1Container(
                          name="init-cu",
                          image="busybox",
                          command=["sh", "/scripts/network-info-cu.sh"],
                          security_context=client.V1SecurityContext(
                              capabilities=client.V1Capabilities(add=["NET_ADMIN"]),
                              run_as_user=0
                          ),
                          volume_mounts=[
                              client.V1VolumeMount(name="config-template-volume",
                                                  mount_path="/config-template"),
                              client.V1VolumeMount(name="config-volume", mount_path="/config"),
                              client.V1VolumeMount(name="script-volume", mount_path="/scripts"),
                          ]
                      )
                  ],
                  containers=[
                      client.V1Container(
                          name="cu",
                          image="ekelhala/srsran-container",
                          command=["srscu"],
                          args=["-c", "/config/cu.yaml"],
                          volume_mounts=[
                              client.V1VolumeMount(name="config-volume", mount_path="/config")
                          ],
                          security_context=client.V1SecurityContext(privileged=True),
                          resources=client.V1ResourceRequirements(
                              requests={"memory": "5Gi"},
                              limits={"memory": "7Gi"}
                          )
                      )
                  ],
                  volumes=[
                      client.V1Volume(
                        name="config-template-volume",
                        config_map=client.V1ConfigMapVolumeSource(name=f"component-configs-{unique_id}")),
                      client.V1Volume(name="config-volume", empty_dir={}),
                      client.V1Volume(name="script-volume",
                                      config_map=client.V1ConfigMapVolumeSource(name="scripts-config")),
                  ]
          )
        )
      )
    )
    return deployment
  except client.exceptions.ApiException as e:
    print(str(e))
    return False
