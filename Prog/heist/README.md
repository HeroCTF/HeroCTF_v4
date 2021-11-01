# Heist

### Category

Prog

### Description

This new online bank is supposely unbreakable. They want us to prove it to the world. Here is the source code. It's messy, but simple. I can feel something's wrong, but I am not sure what.<br>
Help me out will you ?

```
Host : xxxx.heroctf.fr
Port : xxxx
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Files

 - [chall.py](chall.py)

### Write up

The interesting part is the part handling the money transfers : 
```python
def wireMoney(self, amount, receiver):
        if amount > self.balance:
            print("[!] DEBUG MESSAGE : You don't have enough money on your account to make this transfer")
            return False
        else:
            self.balance -= amount
            receiver.balance += amount
            return True
```

The only check is that the entered value shouldn't be greater than the money available on the account. This should provent us to spend money we don't have. But some simple math rules are not taken into account.

What if we passed it a negative number ?

Well the first check is successfully passed, since the amount will be smaller than what is available on the account.

Let's take `-100` as an example, it would translate as :
```python
self.balance = self.balance - (-100)
# self.balance = self.balance + 100
receiver.balance = receiver.balance + (-100)
# receiver.balance = receiver.balance - 100
```

Since there is no check on the receiver's side, you can give yourself illimited money, even if the BANK only has 100€.

Now you just have to buy the flag :)
### Flag

```Hero{ch3ck_4_n3g4t1v3s}```