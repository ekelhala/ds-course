import Router from "express"

import RANResource from "../models/RANResource"
import k8sInteractor from "../k8sInteractor"

const router = Router()

/**
 * Gets the status of resource specified by `id`
 * This view aggregates the data from Kubernetes API and MongoDB
 */
router.get("/:id", async (req, res) => {
    console.log(req.params.id)
    const resourceInDB = await RANResource.findOne({resource_id: req.params.id})
    // processing only if resource in db
    console.log("found resource:", resourceInDB)
    if(resourceInDB) {
        const response = {
            configuration: resourceInDB.toJSON(),
            status: await k8sInteractor.getResourceInfo(req.params.id)
        }
        res.json(response)
    }
    else {
        res.status(404).json({
            error: "Resource not found"
        })
    }
})

export default router