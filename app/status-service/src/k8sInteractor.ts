import kubernetes from "@kubernetes/client-node"

let appsApi: kubernetes.AppsV1Api

/**
 * Initializes this interactor
 */
const init = () => {
    const kubeConfig = new kubernetes.KubeConfig()
    kubeConfig.loadFromCluster()
    appsApi = kubeConfig.makeApiClient(kubernetes.AppsV1Api)
}

/**
 * Returns status of the RAN resource deployment from cluster
 * @param id unique resource id
 */
const getResourceInfo = async (id: string) => {
    const statusInfo = await appsApi.readNamespacedDeploymentStatus({
        namespace: "default",
        name: `srsran-${id}`
    })
    return statusInfo.status
}

export default {
    init,
    getResourceInfo
}