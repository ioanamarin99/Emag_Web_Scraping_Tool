import mongoose from "mongoose"

const Schema = mongoose.Schema

const productSchema = new Schema({
    category : {type:String, required:true},
    name : {type:String, required:true},
    link : {type:String, required:true},
    image_source : {type:String, required:true}
})

const Product = mongoose.model("Product", productSchema)

export default Product