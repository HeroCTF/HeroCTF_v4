#! /usr/bin/python3
def flag():
    flag = "H"
    flag = "e"
    flag = "r"
    flag = "o"
    flag = "{"
    flag = "p"
    flag = "yt"
    flag = "h"
    flag = "0"
    flag = "n"
    flag = "_"
    flag = "4"
    flag = "ss"
    flag = "3mb"
    flag = "l"
    flag = "y"
    flag = "}"


def main():
    user_input = input(">> ")

    filtered = ["import", "os", "sys", "eval", "exec", "__builtins__", "__dict__", "__base__", "__class__", "__subclass__", "dir", "help", "exit"]

    valid_input = True
    for f in filtered:
        if f in user_input:
            print("tssss, what are u doing")
            valid_input = False
            break
    
    if valid_input:
        try:
            exec(user_input, globals(), {'flag':flag})
        except:
            print("You thought I would print errors for u ?")

main()