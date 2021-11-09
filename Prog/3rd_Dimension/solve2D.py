# Dummy solve used to test the necessary puzzle size to avoid little monkeys flagging after running a script for 2 days :)

import time
s = 64

pieces = open("/home/leo/Documents/HeroCTF_v4/Prog/3rd_Dimension/input.txt", "r").readlines()
solution = [[[None for i in range(s)] for i in range(s)] for i in range(s)]
current = (0, 0)

def initStack(pieces):
    stack = []
    for piece in pieces:
        splitted = piece.split("-")
        left = int(splitted[0])
        right = int(splitted[1])
        up = int(splitted[2])
        down = int(splitted[3])
        front = int(splitted[4])
        back = int(splitted[5])
        data = splitted[6]
        stack.append([left, right, up, down, front, back, data])
    return stack

def getFirstPiece(stack):
    ret = None
    for i, piece in enumerate(stack):
        left = piece[0]
        up = piece[2]
        front = piece[3]
        found = False
        for piece2 in stack:
            if piece2[1] == left or piece2[3] == up or piece2[5] == front:
                found = True
                break
        if not found:
            ret = piece
            del piece
            break
        if (i%1000) == 0:
            print(f"{i}/{len(stack)}")
    stack.remove(ret)
    return ret

def getDirection(current):
    if current[0] == 0 and current[1] == 0:
        return "back"
    elif current[0] == 0:
        return "down"
    else:
        return "right"

def getNextPiece(direction, last, stack):
    piece = None
    if direction == "down":
        down = last[3]
        for element in stack:
            if element[2] == down:
                piece = element
                stack.remove(element)
                break
    elif direction == "back":
        back = last[5]
        for element in stack:
            if element[4] == back:
                piece = element
                stack.remove(element)
                break
    else:
        right = last[1]
        for element in stack:
            if element[0] == right:
                piece = element
                stack.remove(element)
                break
    return piece


stack = initStack(pieces)
print("[+] Stack Initilized")
start = time.time()
firstPiece = getFirstPiece(stack)
solution[0][0][0] = firstPiece
current = (1, 0, 0)
print(f"[+] Got First Piece in {time.time() - start}")

while len(stack) > 0:
    direction = getDirection(current)
    #print(direction, current)
    lastPiece = []
    if direction == "right":
        lastPiece = solution[current[0]-1][current[1]][current[2]]
    elif direction == "down":
        lastPiece = solution[current[0]][current[1]-1][current[2]]
    else:
        lastPiece = solution[current[0]][current[1]][current[2]-1]
    nextPiece = getNextPiece(direction, lastPiece, stack)
    solution[current[0]][current[1]][current[2]] = nextPiece
    current = (current[0]+1, current[1], current[2])
    if current[0] == s:
        current = (0, current[1]+1, current[2])
    if current[1] == s:
        current = (0, 0, current[2]+1)
    if len(stack)%s == 0:
        print(f"[+] {len(stack)} pieces left")


flag = ""
for i in range(s):
    flag += solution[i][i][i][-1]

print()
print(f"[+] Flag is : Hero{{{flag}}}")