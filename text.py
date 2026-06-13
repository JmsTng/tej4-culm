import os, time

class Console:
    RESET = "\033[0m"
    
    # Regular
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    GREY = "\033[0;90m"

    # Bold
    BBLACK = "\033[1;30m"
    BRED = "\033[1;31m"
    BGREEN = "\033[1;32m"
    BYELLOW = "\033[1;33m"
    BBLUE = "\033[1;34m"
    BPURPLE = "\033[1;35m"
    BCYAN = "\033[1;36m"
    BWHITE = "\033[1;37m"

    @staticmethod
    def clear(delay: float = 0) -> None:
        """Checks operating system to issue a valid console clear command."""

        time.sleep(delay)
        
        match os.name:
            case "nt": # Windows
                os.system("cls")
            case _: # Linux/MacOS
                os.system("clear")