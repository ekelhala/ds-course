import Router from 'express'

const router = Router()

/**
 * Gets the status of resource specified by `id`
 * This view aggregates the data from Kubernetes API and MongoDB
 */
router.get("/:id", (req, res) => {

})

export default router