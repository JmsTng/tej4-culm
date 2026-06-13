import socket
import subprocess
from datetime import datetime

from battleship import Battleship, Ships
from text import Console


class Player:
    """Base class for abstract functions/shared naming between host and client."""

    def __init__(self):
        self.socket = None
        self.game = Battleship()

        print("AUTOPLACING")
        self.game.place_easy()
        # self.game.place()

    def _procmsg(self, msg: str) -> str:
        """Process message depending on type."""

        match msg[:5]:
            case "COMM:":
                return f"[{datetime.now().strftime('%H%M:%S')}]: {msg[5:]}"
            case "INFO:" | "RSLT:":
                return msg[5:]
            case _:
                return msg

    def sendmsg(self, msg: str) -> None:
        """Send message over socket connection."""

        self.socket.sendall(msg.encode())

    def recvmsg(self, bufsize: int = 1024) -> str:
        """Receive message from socket connection."""

        msg = self.socket.recv(1024).decode()
        out = self._procmsg(msg)

        return out

    def receive_board(self, board: str, ignore_self: bool = False) -> None:
        """Recieve board states."""

        if not board.isnumeric():
            return

        # Split string into opponent board (first half) and self board (second half)
        board_oppo = board[:100]
        board_self = board[100:]

        # Fill out board
        for i in range(100):
            self.game.board_oppo[i // 10][i % 10] = int(board_oppo[i])
            if not ignore_self:
                self.game.board_self[i // 10][i % 10] = int(board_self[i])

    def send_board(self) -> None:
        """Send board states."""

        board = self.game.serialize()
        self.sendmsg("INFO:"+board)

    def make_shot(self) -> str:
        """Fire at a location."""

        shot = ""
        position = (-1, -1)
        free = False
        
        while position == (-1, -1) or not free:
            shot = input("Enter a position (eg. A1): ")
            position = self.game.get_coords(shot)

            if position == (-1, -1):
                Console.clear()
                print(self.game.pretty_print())
                print("That's not in our patrol range, commander! Let's focus somewhere else.")
                continue

            value = self.game.get_value(position, oppo=True)

            if value == self.game.MISS or value == self.game.HIT:
                Console.clear()
                print(self.game.pretty_print())
                print("We've already attacked that spot! Let's aim somewhere else.")
                free = False
                continue

            free = True
            
        return shot


class Host(Player):
    """Host to handle one side of the connection."""

    def __init__(self):
        """Initialize connection. Also keep track of client in case connection drops."""

        super().__init__()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 12345))  # Listen on all interfaces, port 12345

        self.server.listen(1)  # Listen for one connection

        # Retrieve public IP
        cmd1 = subprocess.Popen(["curl", "-s", "ifconfig.me"], stdout=subprocess.PIPE)

        # Retrieve private IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local = s.getsockname()[0]
        s.close()

        # Output IP address for client to connect to
        print(f"Your IPs are:\nPublic: {cmd1.communicate()[0].decode('utf-8').strip()}\nPrivate: {local}")

        # Wait for connection
        self.socket, self.client_ip = self.server.accept()
        self.client_ip = self.client_ip[0]
        print(f"{self.client_ip} {self.recvmsg()}")

        # Reply
        self.sendmsg("COMM:Connected.")

        # Clear screen to begin game
        Console.clear(2)

    def check_win(self) -> str | None:
        """Check if a board has no more boats standing."""

        # Check if client has sunk all of host's ships
        for row in self.game.board_self:
            if not any([False if 0 < _ < 8 else True for _ in row]):
                return "CLIENT"

        # Check if host has sunk all of host's ships
        for row in self.game.board_oppo:
            if not any([False if 0 < _ < 8 else True for _ in row]):
                return "HOST"

    def record_shot(self, position: tuple[int, int], incoming: bool) -> None:
        """Update boards with shot."""

        cell = None
        msg = ""
        
        # Select board to update
        if incoming:
            cell = self.game.board_self[position[0]][position[1]]
            
            # Update
            if cell:
                self.game.board_self[position[0]][position[1]] = self.game.HIT
                if not self.game.find(cell):
                    msg = f" - {Ships(cell).name} SUNK"
            else:
                self.game.board_self[position[0]][position[1]] = self.game.MISS
        else:
            cell = self.game.board_oppo[position[0]][position[1]]
            
            # Update
            if cell:
                self.game.board_oppo[position[0]][position[1]] = self.game.HIT
                if not self.game.find(cell, True):
                    msg = f" - {Ships(cell).name} SUNK"
            else:
                self.game.board_oppo[position[0]][position[1]] = self.game.MISS

        if cell:
            msg = f"HIT on {chr(position[0]+ord('A'))}{position[1]+1}" + msg
        else:
            msg = f"MISS on {chr(position[0]+ord('A'))}{position[1]+1}" + msg
            
        print(msg)
        self.sendmsg("RSLT:"+msg)


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
        self.sendmsg("COMM:Connected.")

        # Recieve response
        print(f"{self.host_ip} {self.recvmsg()}")

        # Clear screen to begin game
        Console.clear(2)
