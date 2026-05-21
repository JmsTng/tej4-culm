import os, socket, subprocess

class Battleship:
    """Base class for abstract functions/shared naming between host and client."""

    def __init__(self):
        self.socket = None
        
    def sendmsg(self, msg):
        self.socket.sendall(msg.encode())

    def recvmsg(self, bufsize: int = 1024) -> str:
        return self.socket.recv(1024).decode()

    @staticmethod
    def clear_console():
        """Checks operating system to issue a valid console clear command."""
        match os.name:
            case "nt":
                os.system("cls")
            case _:
                os.system("clear")

class Host(Battleship):
    """Host to handle one side of the connection."""
    def __init__(self):
        """Initialize connection. Also keep track of client in case connection drops."""

        super()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 12345)) # Listen on all interfaces, port 12345

        self.server.listen(1) # Listen for one connection

        # Output IP address for client to connect to
        cmd1 = subprocess.Popen(["curl", "-s","ifconfig.me"], stdout=subprocess.PIPE)
        print(f"Your IP is: {cmd1.communicate()[0].decode("utf-8").strip()}")

        # Wait for connection
        self.socket, self.client = self.server.accept()

        self.clear_console()
        print(f"{self.client} says: {self.recvmsg()}")

        self.socket.sendall("Connected.".encode())

class Client(Battleship):
    """Client to handle one side of connection."""
    def __init__(self):
        """Initialize SSH connection. Also keep track of host in case connection drops."""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Get host IP address from user
        self.host_ip = input("Enter host IP address: ")

        # Connect to host on port 12345
        self.socket.connect((self.host_ip, 12345))
        self.sendmsg("Connected.")

        # Recieve response
        print(f"{self.host_ip}: {self.recvmsg()}")