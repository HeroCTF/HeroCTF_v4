#! /usr/bin/python3

import os

class account:
    def __init__(self, amount, user):
        self.balance = amount
        self.user = user

    def wireMoney(self, amount, receiver):
        if amount > self.balance:
            print("[!] DEBUG MESSAGE : You don't have enough money on your account to make this transfer")
            return False
        else:
            self.balance -= amount
            receiver.balance += amount
            return True

    def printBalance(self):
        print(f"{self.user} has {self.balance} on his account")

FLAG = open("./flag.txt", "r").read()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Creating the two accounts
ctf_player = account(10, "ctf_player")
BANK = account(100, "Bank")

# Main loop
menu = "dashboard"
while menu != "quit":
    if menu == "dashboard":
        print("=== Dashboard ===")
        print()
        print("Welcome to your HeroBank dashboard ! ")
        print("From here, you can choose to wire money to another account, or to buy some premium features on the HeroStore.")
        print()
        print(f"You currently have {ctf_player.balance}$ on your account")
        print("Choose an option :")
        print("1 - HeroStore")
        print("2 - Transfer money")
        print("3 - Quit")

        option = 0
        try:
            option = int(input(">> "))
            if option == 1:
                menu = "store"
            elif option == 2:
                menu = "transfer"
            elif option == 3:
                menu = "quit"
            else:
                1/0
        except:
            print("An error has occured, enter only 1,2 or 3")
            input("Press enter to continue...")
        clear()

    elif menu == "store":
        print("=== HeroStore ===")
        print()
        print("Welcome to the HeroStore !")
        print("Here you can buy all sorts of things. Sadly, our stocks suffered from our success, and only one item remains. It's therefore pretty expensive.")
        print()
        print("Choose an option :")
        print("1 - Fl4g (100$)")
        print("2 - Back to Dashboard")

        option = 0
        try:
            option = int(input(">> "))
            if option == 1:
                if ctf_player.balance >= 100:
                    print(f"Congratz ! Here is your item : {FLAG}")
                    input("Press enter to continue...")
                    menu = "quit"
                else:
                    print()
                    print("Sorry, but you need more money to make that purchase...")
                    input("Press enter to continue...")
                    menu = "store"
            elif option == 2:
                menu = "dashboard"
            else:
                1/0
        except:
            print("An error has occured, enter only 1 or 2")
            input("Press enter to continue...")
        clear()

    elif menu == "transfer":
        print("=== Transfer Protocol ===")
        print()
        print("How much do you want to transfer the bank ?")
        try:
            amount = int(input(">> "))
            if ctf_player.wireMoney(amount, BANK):
                print("Transfer completed !")
            menu = "dashboard"
            input("Press enter to continue...")
        except:
            print("You have to enter an integer")
            input("Press enter to continue...")
        clear()
