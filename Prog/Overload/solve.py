#!/usr/bin/env python3


with open("overload.txt", "r") as overload:
    content = overload.readline().strip()

    for c in content:
        if not c.isupper():
            print(c, end="")
