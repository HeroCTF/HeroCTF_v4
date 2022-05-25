# Poly321

### Category

Crypto

### Description

An unskilled mathematician has created an encryption function. Can you decrypt the message ?

Format : Hero{flag}<br>
Author : xanhacks

### File

- [encrypt.py](encrypt.py)

### Write up

To decrypt, you can use the bruteforce way as the entry set is small (only chars and symbols).

```python
from string import printable


cipher = [378504, 1040603, 1494654, 1380063, 1876119, 1574468, 1135784, 1168755, 1534215, 866495, 1168755, 1534215, 866495, 1657074, 1040603, 1494654, 1786323, 866495, 1699439, 1040603, 922179, 1236599, 866495, 1040603, 1343210, 980199, 1494654, 1786323, 1417584, 1574468, 1168755, 1380063, 1343210, 866495, 188499, 127550, 178808, 135303, 151739, 127550, 112944, 178808, 1968875]

for c in cipher:
    for p in printable:
        v = ord(p)

        if v + pow(v, 2) + pow(v, 3) == c:
            print(p, end="")
            break
```

Execution :

```
$ python3 decrypt.py
Hero{this_is_very_weak_encryption_92835208}
```

### Flag

`Hero{this_is_very_weak_encryption_92835208}`
