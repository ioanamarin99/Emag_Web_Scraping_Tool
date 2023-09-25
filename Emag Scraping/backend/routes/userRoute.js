import express from 'express'
import User from '../schemas/userSchema.js'
import bcrypt from 'bcrypt'


const router = express.Router()

const BCRYPT_SALT = 10

router.route("/create").post(async (req, res) => {


    const username = req.body.username
    let password = req.body.password

    const hashedPassword = await bcrypt.hash(password, BCRYPT_SALT)

    if (password) {
        password = hashedPassword
        const newUser = new User({ username, password })
        newUser.save().then(() =>
            res.json("New user created")).catch(err => res.status(400).json("Error " + err))
    }
})

router.route("/login").post((req, res) => {
    User.findOne({ username: req.body.username }).then(user => {

        bcrypt.compare(req.body.password, user.password, function (error, response) {
            if (error) {
                res.json("Error")
            }
            if (response) {
                res.json({ _id: user._id })
            }
            else {
                res.json("Invalid password!")
            }
        })

    }).catch(err => res.status(400).json("Error: " + err))
})

export default router