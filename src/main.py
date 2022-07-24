import requests
import os
import sys
import time
import colorama
from colorama import Fore
from utils.files import Files
from security.auth import Auth


class Main:
    def __init__(self):
        self.version = "0.0.1"
        Files.check_Config()
        Auth.check()
        Files.check_TasksDirectory()
        self.menu()

    def ui(self):
        print(Fore.BLUE + "        ____             ______          __")
        print("       / __/__ ____ __ _/_  __/__  ___  / /")
        print("      / _// _ `(_-</ // // / / _ \/ _ \/ / ")
        print("     /___/\_,_/___/\_, //_/  \___/\___/_/  ")
        print("                  /___/                    ")
        print(
            f"                                  v{self.version} \n" + Fore.RESET)

    def menu(self):
        os.system('cls')
        self.ui()
        print(
            f"Happy to see you {Fore.BLUE}{Auth.getDiscordName()}" + Fore.RESET)
        print("What do u want to do ?\n")
        print(f"[ {Fore.BLUE}1{Fore.RESET} ] Start Tasks")
        print(f"[ {Fore.BLUE}2{Fore.RESET} ] Options")
        print(f"[ {Fore.BLUE}e{Fore.RESET} ] Exit\n")
        result = input(">")
        if result == "1":
            pass
        elif result == "2":
            pass
        elif result.lower() == "e":
            print(f"{Fore.BLUE}Exit in 3 secondes..{Fore.RESET}")
            time.sleep(3)
            sys.exit()


Main()
