import {Schema, model} from "mongoose"

const ranResourceSchema = new Schema({
    resource_id: String,
    core_ip: String,
    core_port: String,
    num_rus: Number
}, {
    toJSON: {
        transform: (doc, ret) => {
            delete ret._id
            delete ret.__v
            return ret
        }
    }
})

export default model("RANResource", ranResourceSchema)