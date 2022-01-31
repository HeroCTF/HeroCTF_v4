const express = require('express');
const util = require('util');
const cors = require('cors');
const mysql = require('mysql');
const exec = util.promisify(require('child_process').exec);

const app = express();

var corsOptions = {
    origin: '*',
    optionsSuccessStatus: 200
  }
  
app.get('/test', cors(corsOptions), function (req, res) {
    const { param } = req.query;
    res.status(200).send('This is a test GET endpoint\nPARAM: '+(param || "empty"));
})

app.get("/db_connection", cors(corsOptions), async (req, res) => {
    
    const con = mysql.createConnection({
        host: "localhost",
        user: "player",
        password: "d4AP?5RB7k5My68",
        database: "user_db"
    });
    
    con.connect(function(err) {
        if (err) {
            res.status(500).send("MYSQL: connection error");
        } else {
            con.query("SELECT * FROM USERS", function (err, result, fields) {
                if (err) {
                    res.status(500).send("MYSQL: request error");
                } else {
                    output = "|===== user_db =====|\n|  USER | PASSWORD  |\n|------------------------|\n";
                    result.forEach(element => {
                        output += "| "+element.name + " | " + element.password + " |\n";
                    });
                    output+="|=================|"
                    res.status(200).send(output.trim());
                }
              });
        }
    });
});

app.get('/server_health', cors(corsOptions), async (req, res) => {
    var { timeout,ㅤ} = req.query;
    const checkCommands = [
        '/bin/bash /home/player/scripts/fileIntegrity.sh',
        '/bin/bash /home/player/scripts/isUp.sh localhost:80',
        '/bin/bash /home/player/scripts/isUp.sh localhost:3000',ㅤ
    ];

    var t = 0;
    if (timeout != "") {
        t = parseInt(t);
    }

    try {
        output = ""
        await Promise.all(checkCommands.map(async (cmd) => {
            try {
                r = await exec(cmd, { timeout: t });
                output += r.stdout.trim() || r.stderr.trim();
            } catch (err) {
                output += "";
            }
            output += "\n"
        }));
        res.status(200);
        res.send(output.trim());
    } catch(e) {
        res.status(500);
        res.send('Server status : ERROR');
    }
});

app.listen(3000);