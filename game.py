from battleship import Battleship
from datetime import datetime
from text import Console
import socket, subprocess

class Player:
    """Base class for abstract functions/shared naming between host and client."""

    def __init__(self):
        self.socket = None
        self.game = Battleship()

        self.game.place()
        
    def sendmsg(self, msg: str) -> None:
        """Send message over socket connection."""
        
        self.socket.sendall(msg.encode())

    def recvmsg(self, bufsize: int = 1024) -> str:
        """Receive message from socket connection."""
        
        return f"[{datetime.now().strftime("%H%M:%S")}]: {self.socket.recv(1024).decode()}"

class Host(Player):
    """Host to handle one side of the connection."""
    
    def __init__(self):
        """Initialize connection. Also keep track of client in case connection drops."""

        super().__init__()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 12345)) # Listen on all interfaces, port 12345

        self.server.listen(1) # Listen for one connection

        # Retrieve public IP
        cmd1 = subprocess.Popen(["curl", "-s","ifconfig.me"], stdout=subprocess.PIPE)

        # Retrieve private IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local = s.getsockname()[0]
        s.close()
        
        # Output IP address for client to connect to
        print(f"Your IPs are:\nPublic: {cmd1.communicate()[0].decode("utf-8").strip()}\nPrivate: {local}")

        # Wait for connection
        self.socket, self.client_ip = self.server.accept()
        self.client_ip = self.client_ip[0]
        print(f"{self.client_ip} {self.recvmsg()}")

        # Reply
        self.sendmsg("Connected.")

        # Clear screen to begin game
        Console.clear(2)

class Client(Player):
    """Client to handle one side of connection."""
    
    def __init__(self):
        """Initialize SSH connection. Also keep track of host in case connection drops."""

        super().__init__()
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Get host IP address from user
        self.host_ip = input("Enter host IP address: ")

        # Connect to host on port 12345
        self.socket.connect((self.host_ip, 12345))
        self.sendmsg("Connected.")

        # Recieve response
        print(f"{self.host_ip} {self.recvmsg()}")

        # Clear screen to begin game
        Console.clear(2)
