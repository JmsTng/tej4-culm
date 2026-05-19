import os, socket, subprocess

class Battleship:
    """Base class for abstract functions/shared naming between host and client."""

    @staticmethod
    def clear_console():
        """Checks operating system to issue a valid console clear command."""
        match os.name:
            case "nt":
                os.system("cls")
            case _:
                os.system("clear")
    
class Host(Battleship):
    def __init__(self):
        """Initialize connection. Also keep track of client in case connection drops."""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 12345)) # Listen on all interfaces, port 12345

class Client(Battleship):
    def __init__(self):
        """Initialize SSH connection. Also keep track of host in case connection drops."""