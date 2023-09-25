import express from 'express'
import Product from '../schemas/productSchema.js'

const router = express.Router()

router.route('/list').get((req, res) => {
    Product.find()
        .then(products => res.json(products))
        .catch(err => res.status(400).json("Error: " + err))
})

export default router