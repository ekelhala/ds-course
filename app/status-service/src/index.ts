import Express from "express"
import mongoose from "mongoose"
import k8sInteractor from "./k8sInteractor"

import status from "./routes/status"

const PORT = process.env.PORT || 8000
const app = Express()

mongoose.connect(process.env.MONGODB_URI||"mongodb://127.0.0.1:27017", {
    dbName: "db"
})
    .catch((e) => console.log("Failed connecting to MongoDB: ", e))
    .then(() => console.log("Connected to MongoDB"))
try {
    k8sInteractor.init()
}
catch (error) {
    console.log("Error initializing Kubernetes client:", error)
}

app.use(Express.json())
app.use("/status", status)

app.listen(PORT, () => {
    console.log(`server started on port ${PORT}`)
})