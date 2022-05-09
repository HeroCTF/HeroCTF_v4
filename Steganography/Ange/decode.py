from Crypto.Cipher import AES

algo = AES.new('thisisjustakeyyy', AES.MODE_CBC, '\x7a\xeb\x7e\x7a\x02\xa5\x7f\x77\x40\xfd\xc1\x6d\x6f\xfa\x79\xe7')

with open('redactedHero', "rb") as f:
        d = f.read()

d = algo.encrypt(d)

with open("dec-" + 'unredacted.png', "wb") as f:
        f.write(d)