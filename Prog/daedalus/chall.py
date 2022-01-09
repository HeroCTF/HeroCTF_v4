#! /usr/bin/python3
import os
from secrets import randbelow

FLAG = open("./flag.txt", "r").read()

# Get level names
levels = os.listdir("levels")
firsts = sorted([level for level in levels if level[-1].isdigit()])
randoms = [level for level in levels if level[-1].isalpha()]


# Print the first levels in order, to help player
for i, level in enumerate(firsts):
    data, answer = open(f"levels/{level}", "r").read().split("\n\n")
    print(f"=== {i+1} ===")
    print(data)
    player_answer = input("Answer >> ")
    if answer != player_answer:
        print("Wrong answer... Try again!")
        exit()
    print()

# Print the other levels in a random order
for i in range(len(randoms)):
    print(randbelow(len(randoms)))

print("Congratz !")
print(FLAG)