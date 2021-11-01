# Overload

### Category

Prog

### Description

Find the flag hidden in this `txt` file.

Format : hero{flag}<br>
Author : xanhacks

### Files

- overload.txt

### Write up

To solve this challenge you need to remove all the uppercase characters from the `overload.txt` file.

1. Using a python script to print only not uppercase character :

```python
#!/usr/bin/env python3


with open("overload.txt", "r") as overload:
    content = overload.readline().strip()

    for c in content:
        if not c.isupper():
            print(c, end="")
```

```bash
$ python3 solve.py
hero{wellplayedprogmaster}
```

2. Using bash :

```bash
$ cat overload.txt | tr -d '[:upper:]'
hero{wellplayedprogmaster}
```

### Flag

hero{wellplayedprogmaster}
