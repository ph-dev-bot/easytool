import colorama
from colorama import Fore
from datetime import datetime


class Logger:
    def normal(taskID, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(
            f"{Fore.CYAN}[{current_time}][TASK {taskID}] {message}{Fore.RESET}")

    def mid(taskID, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(
            f"{Fore.MAGENTA}[{current_time}][TASK {taskID}] {message}{Fore.RESET}")

    def error(taskID, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(
            f"{Fore.RED}[{current_time}][TASK {taskID}] {message}{Fore.RESET}")

    def success(taskID, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(
            f"{Fore.GREEN}[{current_time}][TASK {taskID}] {message}{Fore.RESET}")
