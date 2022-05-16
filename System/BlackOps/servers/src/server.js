#! /usr/bin/node

const path = require('path')
const express = require(path.join(__dirname, "..", "libs", "node_modules", "express"))
const app = express()

app.get('/', function (req, res) {
  res.send('Hello World')
})

app.listen(9091)