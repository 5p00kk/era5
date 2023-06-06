from enum import Enum
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

class Logger_level(Enum):
    DEBUG = 1
    INFO = 2
    WARN = 2
    ERROR = 3

    def __eq__(self, other):
        if isinstance(other, Logger_level):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Logger_level):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Logger_level):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Logger_level):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Logger_level):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            return NotImplemented

class Logger:

    def __init__(self, lvl=Logger_level.DEBUG) -> None:
        self.lvl = lvl

    def set_level(self, lvl):
        self.lvl = lvl

    def error(self, text):
        if self.lvl <= Logger_level.ERROR:
            print(f"{Fore.RED}<E> {text}{Style.RESET_ALL}")

    def warn(self, text):
        if self.lvl <= Logger_level.WARN:
            print(f"{Fore.YELLOW}<W> {text}{Style.RESET_ALL}")

    def info(self, text):
        if self.lvl <= Logger_level.INFO:
            print(f"{Fore.GREEN}<I> {text}{Style.RESET_ALL}")

    def debug(self, text):
        if self.lvl <= Logger_level.DEBUG:
            print(f"{Fore.BLUE}<D> {text}{Style.RESET_ALL}")