# pyjAil iS Mad

### Category

Misc

### Description

The pyjail isn't designed to pop a shell, or read a file. Just recover the redacted part of the source code.


**Host** : misc.heroctf.fr<br>
**Port** : 6000


Format : **Hero{flag}**<br>
Author : **Log_s**

### Files

- [pyjail_redacted.py](pyjail_redacted.py)

### Write up

Our goal is to recover the `flag()` function that was redacted.

Notice that flag is the only function that is loaded in the environment where the user commands are ran.
```python
exec(user_input, {"__builtins__": {}}, {'flag':flag})
```

It's indeed possible to execute it, not like every other functions.
```
$ ./pyjail.py                                                                    
>> print
You thought I would print errors for u ?
>> flag
>> flag()
```

There is no output though.

There are ways to recover a python function's code, but it requires importing a library, which is not possible here.

It's howerver possible to recover the `__code__` object from a function.

Here is an example:
```
>>> def test():
...     return 1+1
... 
>>> dir(test)
['__annotations__', '__builtins__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> test.__code__.co_code
b'd\x01S\x00'
```

The last line is the assembly code corresponding to the function `test()`.
For exemple, the first byte which is translated to `d` corresponds to the opcode 0x64, which is LOAD_CONST (ord(d) == 100 == 0x64). The second one indicated to load the consts at index 0x01 (which is 2), and the last one (ord(S) == 0x53) is the opcode for RETURN_VALUE.

If we try this in the jail, no error is risen, but we don't have any output either. Indeed, the jail excutes the code, but does not print anything, and the print function is not available to us.

The way here, is to extract the data character by character, by triggering and error when the right one is found, with an input like this one.

```python
if flag.__code__.co_code[0]==0x64:1/0
```

Example in the jail:
```
>> if flag.__code__.co_code[0]==0x64:1/0
You thought I would print errors for u ?
>> if flag.__code__.co_code[0]==0x65:1/0
>>
```
The error is risen for 0x64 value, which is the first byte of the assembly code.

Let's extract the entire assembly code:
```python
from pwn import *

p = process("./pyjail.py")
p.recvuntil(b">> ")

### Extract assembly code
asm_code, found, index = [], True, 0
while found:
    for x in range(256):
        found = False
        p.sendline(f"if flag.__code__.co_code[{index}]=={x}:1/0".encode())
        res = p.recvuntil(b">> ").decode()
        if "errors" in res:
            # If error on opcode 0, check the next to see if the error is because we found the correct opcode
            # or because of index error
            if x == 0:
                p.sendline(f"if flag.__code__.co_code[{index}]=={x+1}:1/0".encode())
                res = p.recvuntil(b">> ").decode()
                if "errors" in res:
                    found = False
                    break
            asm_code.append(hex(x))
            found = True
            break
    index += 1

print(asm_code)
```

If you take a look at the outputed assembly, there are a lot of LOAD_CONST calls (0x64).
```
['0x64', '0x1', '0x7d', '0x0', '0x64', '0x2', '0x7d', '0x0', '0x64', '0x3', '0x7d', '0x0', '0x64', '0x4', '0x7d', '0x0', '0x64', '0x5', '0x7d', '0x0', '0x64', '0x6', '0x7d', '0x0', '0x64', '0x7', '0x7d', '0x0', '0x64', '0x8', '0x7d', '0x0', '0x64', '0x9', '0x7d', '0x0', '0x64', '0xa', '0x7d', '0x0', '0x64', '0xb', '0x7d', '0x0', '0x64', '0xc', '0x7d', '0x0', '0x64', '0xd', '0x7d', '0x0', '0x64', '0xe', '0x7d', '0x0', '0x64', '0xf', '0x7d', '0x0', '0x64', '0x10', '0x7d', '0x0', '0x64', '0x11', '0x7d', '0x0', '0x64', '0x0', '0x53', '0x0']
```

The referred consts are stored in the `co_consts` attribute of the `__code__` object.

Let's extract them in a similar way:
```python
asm_consts, found, index = [], True, 1
charset = string.ascii_letters + string.digits + "_{}" # Typicall flag charset
while found:
    for x in range(len(charset)):
        found = False
        p.sendline(f"if flag.__code__.co_consts[{index}][0]=='{charset[x]}':1/0".encode())
        res = p.recvuntil(b">> ").decode()
        if "errors" in res:
            # If error on opcode 0, check the next to see if the error is because we found the correct opcode
            # or because of index error
            if x == 0:
                p.sendline(f"if flag.__code__.co_consts[{index}][0]=='{charset[x+1]}':1/0".encode())
                res = p.recvuntil(b">> ").decode()
                if "errors" in res:
                    found = False
                    break
            asm_consts.append(charset[x])
            found = True
            break
    index += 1

print("".join(asm_consts))
```

By only doing this, the result is `Hero{pyh0n_4s3ly}`. It doesn't validate the challenge, and there seems to be some characters missing.

The consts are actually more than one char long (yes I am evil).

Let's tweak the code a bit
```python
asm_consts, found, index, round_with_0_char = [], True, 1, 0
charset = string.ascii_letters + string.digits + "_{}" # Typicall flag charset
while True:
    offset = 0
    valid_offset = True
    while valid_offset:
        for x in range(len(charset)+1):
            found = False
            p.sendline(f"if flag.__code__.co_consts[{index}][{offset}]=='{charset[x]}':1/0".encode())
            res = p.recvuntil(b">> ").decode()
            if "errors" in res:
                # If error on opcode 0, check the next to see if the error is because we found the correct opcode
                # or because of index error
                if x == 0:
                    p.sendline(f"if flag.__code__.co_consts[{index}][{offset}]=='{charset[x+1]}':1/0".encode())
                    res = p.recvuntil(b">> ").decode()
                    if "errors" in res:
                        round_with_0_char += 1
                        valid_offset = False
                        break
                asm_consts.append(charset[x])
                offset += 1
                round_with_0_char = 0
                break
    index += 1
    if round_with_0_char == 2:
        break

print("".join(asm_consts))
```

The code is almost the same. The only difference in the usage of the `round_with_0_char` that checks if we did 2 loops that outputed 0 chars (in which case we are at the end of the co_consts n-uple).

Well done ! Maybe next time you'll get to reverse some python assembly code ;).

### Flag

```
Hero{pyth0n_4ss3mbly}
```
