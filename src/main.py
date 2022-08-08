import requests
import os
import sys
import time
import csv
import glob
import colorama
from colorama import Fore
from utils.files import Files
from security.auth import Auth
from security.anti_debug import AntiDebug
import threading
from modules.zalando.subscriber import zalandoSubscriber


class Main:
    def __init__(self):
        self.version = "0.0.1"
        os.system('cls')
        #threading.Thread(target=AntiDebug().ok, args=()).start()
        # Files.check_Config()
        # Auth.check()
        # Files.check_TasksDirectory()
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
        # print(
        #    f"Happy to see you {Fore.BLUE}{Auth.getDiscordName()}" + Fore.RESET)
        print("What do u want to do ?\n")
        print(f"[ {Fore.BLUE}1{Fore.RESET} ] Modules")
        print(f"[ {Fore.BLUE}2{Fore.RESET} ] Options")
        print(f"[ {Fore.BLUE}e{Fore.RESET} ] Exit\n")
        result = input(">")
        if result == "1":
            self.modulesMenu()
        elif result == "2":
            pass
        elif result.lower() == "e":
            print(f"{Fore.BLUE}Exit in 3 secondes..{Fore.RESET}")
            time.sleep(3)
            os._exit(1)
        else:
            self.menu()

    def modulesMenu(self):
        os.system('cls')
        self.ui()
        print("What do u want to do ?\n")
        print(f"[ {Fore.BLUE}1{Fore.RESET} ] Zalando")
        print(f"[ {Fore.BLUE}b{Fore.RESET} ] Back\n")
        result = input(">")
        if result == "1":
            path = r'Tasks/zalando/*.csv'
            files = glob.glob(path, recursive=True)
            if len(files) == 0:
                print(f"{Fore.RED}No Tasks Files Found !{Fore.RESET}")
                self.menu()
            else:
                os.system('cls')
                self.ui()
                i = 0
                for file in files:
                    print(
                        f"[ {Fore.BLUE}{i}{Fore.RESET} ] {os.path.basename(file)}")
                selectionFile = int(
                    input(f"\n{Fore.BLUE}Select your files: {Fore.RESET}"))

                if selectionFile > len(files):
                    print(f"{Fore.RED}Wrong Number!{Fore.RESET}")
                    time.sleep(3)
                else:
                    task_reader = csv.DictReader(
                        open(files[selectionFile], 'r'))
                    activeTasks = []
                    for z, task in enumerate(task_reader):
                        if task_reader.line_num == 1:
                            continue
                        else:
                            mode = task["mode"]
                            email = task["email"]
                            password = task["password"]
                            country = task["country"]
                            newPassword = task["newPassword"]
                            firstname = task["firstname"]
                            lastname = task["lastname"]
                            street = task["street"]
                            zipcode = task["zip"]
                            city = task["city"]
                            useProxy = task["useProxy"]
                            if mode.lower() == "subscriber":
                                t = threading.Thread(target=zalandoSubscriber, args=(
                                    str(z), email, password, country, firstname, lastname, street, zipcode, city, useProxy,))
                                activeTasks.append(t)
                                t.start()
                    for t in activeTasks:
                        t.join()
                        # zalandoSubscriber("1", "przemo120472@interia.pl",
                        #                  "Marcel13012006", "fr", "true")
        elif result.lower() == "b":
            self.menu()
        else:
            self.modulesMenu()


Main()
