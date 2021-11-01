#!/usr/bin/env python3
from os import getenv
from random import randint, choice
from string import ascii_uppercase

flag = getenv("FLAG") if getenv("FLAG") else "heroctf{wellplayedprogmaster}"
min_number, max_number = 10, 100


def generate_random_string():
    length = randint(min_number, max_number)
    return "".join([choice(ascii_uppercase) for _ in range(length)])


for c in flag:
    print(generate_random_string(), end="")
    print(c, end="")
    print(generate_random_string(), end="")
