# TODO : make sure corners are centered

import secrets
from puzzle import Piece
import uuid

flag = "7d17bb62491b3abba957b7d6ab6795d6d7a0531c3fc6a6d68449a4693b91416b"
size = len(flag) #64
charset = "0123456789abcdef"

puzzle = []

print("[*] Create puzzle with embedded flag")
# Create puzzle with embedded flag
for i in range(size):
    puzzle.append([])
    for j in range(size):
        puzzle[i].append([])
        for k in range(size):
            if i == j == k:
                p = Piece()
                p.data = flag[i]
                puzzle[i][j].append(p)
            else:
                p = Piece()
                p.data = secrets.choice(charset)
                puzzle[i][j].append(p)

print("[*] Split puzzle in pieces with random IDs")
# Split puzzle in pieces with random IDs
for i in range(size):
    for j in range(size):
        for k in range(size):

            if not puzzle[i][j][k].left:
                left = uuid.uuid1().int
                puzzle[i][j][k].left = left
                if i>0 and not puzzle[i-1][j][k].right:
                    puzzle[i-1][j][k].right = left

            if not puzzle[i][j][k].right:
                right = uuid.uuid1().int
                puzzle[i][j][k].right = right
                if i<size-1 and not puzzle[i+1][j][k].left:
                    puzzle[i+1][j][k].left = right

            if not puzzle[i][j][k].top:
                top = uuid.uuid1().int
                puzzle[i][j][k].top = top
                if j>0 and not puzzle[i][j-1][k].bottom:
                    puzzle[i][j-1][k].bottom = top

            if not puzzle[i][j][k].bottom:
                bottom = uuid.uuid1().int
                puzzle[i][j][k].bottom = bottom
                if j<size-1 and not puzzle[i][j+1][k].top:
                    puzzle[i][j+1][k].top = bottom

            if not puzzle[i][j][k].front:
                front = uuid.uuid1().int
                puzzle[i][j][k].front = front
                if k>0 and not puzzle[i][j][k-1].back:
                    puzzle[i][j][k-1].back = front

            if not puzzle[i][j][k].back:
                back = uuid.uuid1().int
                puzzle[i][j][k].back = back
                if k<size-1 and not puzzle[i][j][k+1].front:
                    puzzle[i][j][k+1].front = back

print("[*] Convert to single dimension list")
# Write data
lines = []
for i in range(size):
    for j in range(size):
        for k in range(size):
            if len(lines) > 0:
                lines.insert(secrets.choice(range(len(lines))), puzzle[i][j][k])
            else:
                lines.append(puzzle[i][j][k])

print("[*] Format text data")
toWrite = ""
for i, line in enumerate(lines):
    lineToWrite = f"{line.left}-{line.right}-{line.top}-{line.bottom}-{line.front}-{line.back}-{line.data}\n"
    toWrite += lineToWrite

print("[*] Write data")
with open("input.txt", "w") as f:
    f.write(toWrite)

print()
print("[+] Puzzle is created!")
