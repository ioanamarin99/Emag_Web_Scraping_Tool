import express from 'express'
import cors from 'cors'
import mongoose from 'mongoose'
import dotenv from 'dotenv'
import * as child from 'child_process'

import productRouter from './routes/productRoute.js'
import userRouter from './routes/userRoute.js'


const childPython = child.spawn('python',["emagScraping.py"])
childPython.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
})

childPython.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
})

childPython.on("close",(code) => {
    console.log(`exited with code ${code}`)
})
dotenv.config()

const app = express()

const port = process.env.PORT || 5000
const uri = "mongodb+srv://ioana:scraper123@cluster0.v8fml.mongodb.net/scraper?retryWrites=true&w=majority"

app.use(cors())
app.use(express.json())

mongoose.connect(uri)

const connection = mongoose.connection

connection.once('open', function () {
    console.log("MongoDB connected successfully!")
})

app.use('/user', userRouter)
app.use('/products', productRouter)

app.listen(port, function () {
    console.log("Server running on port " + port)
})