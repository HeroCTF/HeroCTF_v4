#! /usr/bin/python3

def flag():
    # REDACTED
    # THIS FUNCTION DOES NOT PRINT OR RETURN ANYTHING
    pass


def jail():
    user_input = input(">> ")

    filtered = ["import", "os", "sys", "eval", "exec", "__builtins__", "__dict__", "__base__", "__class__", "__subclass__", "dir", "help", "exit", "open", "read"]

    valid_input = True
    for f in filtered:
        if f in user_input:
            print("tssss, what are u doing")
            valid_input = False
            break
    
    if valid_input:
        try:
            exec(user_input, {"__builtins__": {}}, {'flag':flag})
        except:
            print("You thought I would print errors for u ?")

if __name__ == "__main__":
    try:
        while True:
            jail()
    except KeyboardInterrupt:
        print("Bye")