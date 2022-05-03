# Deadalus

### Category

Prog

### Description

Deadalus has lost the technical information of his famous maze and is left with a few old blueprints. He want's to add some improvements to it but got lost along the way. If you could just help him count the number of unique loops in different parts of the maze, it would be... amazing ?

The maze is magic, so there is no notion of walls and corridors, but there are gateways that allow you to travel in a direction (`L`: left, `R`: right, `U`: up, `D`: down). Some gateways are special, and allow you to go in two opposit directions (`-`: left/right, `|`: up/down).

If a gateway leads to another part of the maze (-> it leads outside of the grid), the loop is not complete, so don't count it. The same loop can't go twice through the same special getaway to go in both directions, it automatically leads to two different loops.
```
. R . D . .
R . . . . D
. | . L . .
. . . . . .
. R . U . .
```
In the previsous example, there are two unique loops. There are detailed on the following figure. The two first are the two unique loops, as for the third, it's not complete.
```
. ----- . .   . . . . . .   . . . . . .
. | . | . .   . . . . . .   -----------
. ----- . .   . ----- . .   . . . . . |
. . . . . .   . | . | . .   . . . . . |
. . . . . .   . ----- . .   . . . . . |
```
Finaly, you can use special gateways in a specific direction only. Here are two examples, the first where you can use the gateway, the second were you can not.
```
. . . . . .   . . . ^ . .  |  . . . . . .   . . . . . .
. . . . . .   . . . | . .  |  . . . . . .   . . . . . .
. R . | . .   . ->. | . .  |  . R . - . .   . ->. X . .
. . . . . .   . . . | . .  |  . . . . . .   . . . . . .
. . . . . .   . . . v . .  |  . . . . . .   . . . . . .
```
NB: to help you, the first 6 maze parts are always the same, and covering the basics. The next maze parts are random.
```
Host : xxxx.heroctf.fr
Port : xxxx
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write up

The following script allows you to solve the challenge. If the comments are not clear enough, you can contact me on discord for a more detailed explanation.
```python
from copy import deepcopy
from pwn import *



host = "localhost"
port = 7002



def getNext(grid, x, y):
    h,w = len(grid), len(grid[0])
    # Depending on the symbole, loop until we hit the grid's border, or another symbol
    match grid[y][x]:
        case "R":
            for p in range(1, w-x):
                if grid[y][x+p] != ".":
                    return x+p, y
        case "L":
            for p in range(1, x+1):
                if grid[y][x-p] != ".":
                    return x-p, y
        case "D":
            for p in range(1, h-y):
                if grid[y+p][x] != ".":
                    return x, y+p
        case "U":
            for p in range(1, y+1):
                if grid[y-p][x] != ".":
                    return x, y-p
    # If no symbol has been returned, return (-1, -1) to indicate we hit a border
    return -1, -1

def find(grid, x, y, loop=None):
    # If it's the first call, create an empty list
    if loop == None:
        loop = []
    
    # Add current node to list
    loop.append((x, y))

    # Get the coordinates of the of the next symbole, (-1, -1) if the border was hit)
    nx, ny = getNext(grid, x, y)

    if (nx, ny) == (-1, -1): # Border was hit
        return None

    elif (nx, ny) == (loop[0][0], loop[0][1]): # Back to first node, end of recursivity
        return sorted(loop)

    elif (nx, ny) in loop: # Already encountered node, but not the first, provent infinite loop
        return None

    elif grid[ny][nx] in ["R", "L", "U", "D"]: # New node, subcall
        return find(grid, nx, ny, loop)

    else:  # Special gateways
        loop.pop()
        grid1 = deepcopy(grid)
        grid2 = deepcopy(grid)

        if grid[ny][nx] == "-": # for -
            if grid[y][x] in ["R", "L"]: # Don't count if arriving from left or right
                return None
            grid1[ny][nx] = "R"
            grid2[ny][nx] = "L"

        else: # for |
            if grid[y][x] in ["U", "D"]: # Don't count if arriving from up or down
                return None
            grid1[ny][nx] = "U"
            grid2[ny][nx] = "D"

        loop1 = find(grid1, x, y, deepcopy(loop))
        loop2 = find(grid2, x, y, deepcopy(loop))

        # Choose the grid to return
        if loop1 == None and loop2 == None:
            return None
        elif loop1 == None:
            return loop2
        else:
            return loop1

def count_loops(grid):
    h, w = len(grid), len(grid[0])
    loops = []

    for y in range(h):
        for x in range(w):
            if grid[y][x] != ".":
                l = find(grid, x, y)
                if l not in loops and l != None:
                    loops.append(l)

    return len(loops)

def get_grid(socket):
    data = socket.recvuntil(b"Answer >> ").decode()
    print(data)
    grid_raw = data.split("===")[2].split("Answer >> ")[0].strip()
    lines = grid_raw.split("\n")
    grid = []
    for line in lines:
        grid.append([x for x in line])
    return grid


if __name__ == "__main__":
    r = remote(host, port)

    for i in range(6):
        grid = get_grid(r)
        nb_loops = str(count_loops(grid))
        r.sendline(nb_loops.encode())
        print(nb_loops)
```

### Flag

```Hero{h0w_aM4ZEiNg_y0U_d1D_17_3v3n_beTt3R_th4n_4ri4dne}```
