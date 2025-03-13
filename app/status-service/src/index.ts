import Express from 'express'

import status from "./routes/status"

const PORT = process.env.PORT || 8000

const app = Express()

app.use("/status", status)

app.listen(PORT, () => {
    console.log(`server started on port ${PORT}`)
})