import Express from "express"
import mongoose from "mongoose"
import k8sInteractor from "./k8sInteractor"

import status from "./routes/status"

const PORT = process.env.PORT || 8000
const app = Express()

mongoose.connect(process.env.MONGODB_URI||"mongodb://127.0.0.1:27017")
    .catch((e) => console.error("Failed connecting to MongoDB: ", e))
    .then(() => console.log("Connected to MongoDB"))
k8sInteractor.init()

app.use(Express.json())
app.use("/status", status)

app.listen(PORT, () => {
    console.log(`server started on port ${PORT}`)
})