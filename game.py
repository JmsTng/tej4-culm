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

        self.socket.listen(1) # Listen for one connection

        # Output IP address for client to connect to
        cmd1 = subprocess.Popen(["ip", "a"], stdout=subprocess.PIPE)
        cmd2 = subprocess.Popen(["grep", "wlan"], stdin=cmd1.stdout, stdout=subprocess.PIPE)
        cmd3 = subprocess.Popen(["grep", "inet"], stdin=cmd2.stdout, stdout=subprocess.PIPE)

        print(f"Your IP is: {cmd3.communicate()[0]}")

class Client(Battleship):
    def __init__(self):
        """Initialize SSH connection. Also keep track of host in case connection drops."""