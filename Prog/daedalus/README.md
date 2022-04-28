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

### Flag

```Hero{h0w_aM4ZEiNg_y0U_d1D_17_3v3n_beTt3R_th4n_4ri4dne}```