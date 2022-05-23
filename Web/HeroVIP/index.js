let express = require('express')
let app = express()
let cp = require('cookie-parser');
let session = require('express-session')
var bodyParser = require('body-parser')
let path = require("path")
let crypto = require('crypto');
var uuid = require('uuid');
var serialize = require('node-serialize');
require('express-ws')(app);
let usersModel = require("./helpers/UsersModel");
let functions = require("./helpers/functions")
let sqlite3 = require('sqlite3')
const { base64encode, base64decode } = require('nodejs-base64');
const port = 3000
app.use(cp());
app.use(bodyParser())
let db = new sqlite3.Database('./presales.sqlite3');

app.use(session({
    secret: functions.generateRandomString(),
    resave: false,
    saveUninitialized: true
}))

app.get("/",(req,res) => {
    if(req.session.name !== undefined) res.redirect("/queue");
    else res.sendFile(path.join(__dirname+'/templates/index.html'));
})

app.post("/api/v1/register", async (req,res) => {
    if(req.body.alias !== undefined && req.body.pwd !== undefined)
    {
        if(req.body.alias.length <= 100 && /^[a-zA-Z0-9]+$/.test(req.body.alias))
        {
            let possibleUser,err;
            await usersModel.selectUser(req.body.alias).then((resp) => {possibleUser = resp}).catch((resp) => {err = resp})
            if(err)
            {
                res.json({'err':'Unknown error occured, please try again'})
                res.end()
            }else
            {
                if(possibleUser.length === 0)
                {
                    const hash = crypto.createHash('sha256').update(req.body.pwd).digest('base64');
                    let resInsert;
                    await usersModel.insertUser(req.body.alias,hash).then((resp) => {resInsert = resp}).catch((resp) => {err = resp})
                    if(err)
                    {
                        res.json({'err':'Unknown error occured, please try again'})
                        res.end()
                    }else
                    {
                        if(res)
                        {
                            res.json({'ok':'user created'})
                            res.end()
                        }else{
                            res.json({'err':'Unknown error occured, please try again'})
                            res.end()
                        }
                    }
                }else
                {
                    res.json({"err":"This user already exist."})
                    res.end()
                }
            }
        }else
        {
            res.json({"err":"Alias must be at least 100 caracters or you provide invalid caracters"})
            res.end()
        }
    }else
    {
        res.json({"err":"Missing parameters"})
        res.end()
    }
})

app.post("/api/v1/login", async (req,res) => {
    if(req.body.alias !== undefined && req.body.pwd !== undefined)
    {
        let possibleUser,err;
        await usersModel.selectUser(req.body.alias).then((resp) => {possibleUser = resp}).catch((resp) => {err = resp})
        if(err)
        {
            res.json({'err':'Unknown error occured, please try again'})
            res.end()
        }else
        {
            if(possibleUser.length > 0)
            {
                const hash = crypto.createHash('sha256').update(req.body.pwd).digest('base64');
                if(hash === possibleUser[0]['password'])
                {
                    req.session.name = possibleUser[0]['alias'];
                    res.json({'ok':'user connected'})
                    res.end()
                }else
                {
                    res.json({'err':'Alias or password is incorrect'})
                    res.end();
                }
            }else
            {
                res.json({'err':'Alias or password is incorrect'})
                res.end();
            }
        }
    }else
    {
        res.json({"err":"Missing parameters"})
        res.end()
    }
})

app.post("/api/v1/form",async (req,res) => {
    let resAccess = await functions.canAccessForm(usersModel, req)
    if(req.session.name !== undefined && resAccess)
    {
        if(req.body.email !== undefined && req.body.status !== undefined)
        {
            let data = {"email":req.body.email, "status":req.body.status}
            if(req.body.commentary !== undefined) data["commentary"] = req.body.commentary
            data = serialize.serialize(data)
            let newCook = base64encode(data)
            res.cookie('completedForm',newCook)
            res.json({"ok":"Form created but you have to wait for the form to be validated by administrators"})
        }else res.json({"err":"Missing parameters"})
    }else res.json({"err":"Unauthorized"})
})

app.get("/myform", async (req,res) => {
    let resAccess = await functions.canAccessForm(usersModel, req)
    if(req.session.name !== undefined && resAccess)
    {
        if(req.cookies !== undefined && req.cookies['completedForm'] !== undefined)
        {
            try{
                var obj = serialize.unserialize(base64decode(req.cookies['completedForm']))
                console.log(obj)
                if(obj.commentary) res.json({"email":obj.email,"status":obj.status,"commentary":obj.commentary})
                else res.json({"email":obj.email,"status":obj.status})
            }catch(e){
                console.log(e)
                res.json({"err":"An error occured, please try again"})
            }
        }else res.redirect("/form")
    }else res.redirect("/")
})

app.get("/form", async (req,res) => {
    let resAccess = await functions.canAccessForm(usersModel, req)
    if(resAccess && req.cookies !== undefined && req.cookies['completedForm'] !== undefined) res.redirect("/myform")
    if(req.session.name !== undefined && resAccess) res.sendFile(path.join(__dirname+'/templates/form.html'));
    else res.redirect("/")
})

app.get("/queue", async (req,res) => {
    let resAccess = await functions.canAccessForm(usersModel, req)
    if(resAccess)
    {
        res.redirect("/form")
        res.end()
    }else
    {
        if(req.session.name !== undefined && resAccess === false) res.sendFile(path.join(__dirname+'/templates/queue.html'));
        else res.redirect("/");
    }
})

app.ws('/ws',function(ws, req) {
    ws.on('message', async function(msg)
    {
        if(msg == "join")
        {
            if(req.session.name !== undefined)
            {
                if(req.session.queueId === undefined)
                {
                    db.all('SELECT uuid FROM queue WHERE associateUser = ?',req.session.name, (err, rows)=>{
                        if(rows.length > 0) req.session.queueId = rows[0]['uuid']
                        else
                        {
                            let queueId = uuid.v4();
                            db.run('INSERT INTO queue(uuid, associateUser, origin, lastUpdate, percentage, numberOfRequest) VALUES(?, ?, ?, 1990-01-01, 0, 1)',[queueId,req.session.name,req['host']], (err) => 
                            {
                                if(err) ws.send(JSON.stringify({"err":"Error while trying to join queue"}))
                                else ws.send(JSON.stringify({"ok":0}))
                            })
                            req.session.queueId = queueId
                        }
                    })
                }else ws.send(JSON.stringify({"err":"User have already join the queue: "+req.session.queueId}))
            }else ws.send(JSON.stringify({"err":"User not connected"}))
        }else
        {
            if(msg.includes("update"))
            {
                if(req.session.queueId !== undefined)
                {
                    db.all("SELECT numberOfRequest, origin, lastUpdate, percentage,numberOfRequest FROM queue WHERE associateUser = ?",[req.session.name], function(err,rows)
                    {
                        if(err) ws.send("Something went wrong, try again")
                        else
                        {
                            if(rows.length > 0)
                            {
                                if(rows[0]['origin'] === req['host'])
                                {
                                    let lastUpdate = new Date(rows[0]['lastUpdate'])
                                    let percentage = rows[0]['percentage']
                                    let numberOfRequest = ""
                                    if(isNaN(parseInt(msg.split("/")[1]))) numberOfRequest = msg.split("/")[1]
                                    else numberOfRequest = rows[0]['numberOfRequest']
                                    let now = new Date()
                                    if(now - lastUpdate >= lastUpdate.setTime(lastUpdate.getTime() + 60 * 60 * 1000)) percentage += 1
                                    if(percentage >= 100)
                                    {
                                        usersModel.updateUser(req.session.name)
                                        ws.send(JSON.stringify({"finish":"Queue finished ! You can join the form at /form !"}))
                                    }else
                                    {
                                        try
                                        {
                                            db.run("UPDATE queue SET lastUpdate = '"+new Date()+"', percentage = '"+percentage+"', numberOfRequest = '"+numberOfRequest+"' WHERE associateUser = '"+req.session.name+"'", (err) => 
                                            {
                                                if(err) ws.send(JSON.stringify({"err":"An error occured, try again"}))
                                                else ws.send(JSON.stringify({"ok":percentage,"numberOfRequest":numberOfRequest}))
                                            })
                                        }catch(e)
                                        {
                                            ws.send(JSON.stringify({"err":"An error occured while processing message, please try again"}))
                                        }
                                    }
                                }else ws.send(JSON.stringify({"err":"Not the same origin as registered, unauthorized"}))
                            }else ws.send(JSON.stringify({"err":"User not found in queue"}))
                        }
                    })
                }else ws.send(JSON.stringify({"err":"User not connected or not in current queue"}))
            }else ws.send(JSON.stringify({"err":"Command not handled"}))
        }
    })
})                        

app.listen(port, () => 
{
    console.log(`App listening at http://localhost:${port}`)
})