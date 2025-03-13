import Express from 'express'

const PORT = process.env.PORT || 8000

const app = Express()



app.listen(PORT, () => {
    console.log(`server started on port ${PORT}`)
})