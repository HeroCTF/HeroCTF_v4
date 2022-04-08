#! /usr/bin/python3.10
import os
from secrets import choice, randbelow
from solve import count_loops

FLAG = open("./flag.txt", "r").read()


def generate_grid():
    b1, b2 = 30, 40
    m = 10

    s = randbelow(b2-b1) + b1
    g = [["" for x in range(s)] for x in range (s)]
    chars = ["-", "|", "R", "L", "U", "D"]
    chars += ["."]*(len(chars)*m)

    for y in range(s):
        for x in range(s):
            g[y][x] = choice(chars)

    return g



# Get level names
levels = sorted(os.listdir("levels"))
print(levels)
counter = 1

# Print the first levels in order, to help player
for level in levels:
    data, answer = open(f"levels/{level}", "r").read().split("\n\n")
    print(f"=== {counter} ===")
    print(data)
    player_answer = input("Answer >> ").strip()
    if answer != player_answer:
        print("Wrong answer... Try again!")
        exit()
    print()
    counter += 1

# Print the other levels (randomly generated)
for i in range(10):
    grid = generate_grid()
    answer = str(count_loops(grid))
    grid_str = ""
    for line in grid:
        grid_str += "".join(line)+"\n"
    print(f"=== {counter} ===")
    print(grid_str)
    player_answer = input("Answer >> ").strip()
    if answer != player_answer:
        print("Wrong answer... Try again!")
        exit()
    print()
    counter += 1


print("Congratz !")
print(FLAG)