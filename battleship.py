from enum import Enum
from getkey import getkey, keys
from typing_extensions import Literal

class Ships(Enum):
    """Collect ship types in an enumerable."""

    CARRIER = 1
    BATTLESHIP = 2
    CRUISER = 3
    SUBMARINE = 4
    DESTROYER = 5

class Battleship:
    def __init__(self, rows: int = 10, cols: int = 10):
        self.ROWS = rows
        self.COLS = cols
        self.board_self = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.board_oppo = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def validate_position(self, position: str) -> Literal[False] | tuple[int, int]:
        """Check that a given position is within board boundaries."""

        row, col = list(position[:2])

        try:
            row = ord(row.upper()) - ord("A")
            col = int(col) - 1

            if 0 < row < self.ROWS and 0 < col < self.COLS:
                return (row, col)
            print("That's not in our patrol range, commander! Let's focus somewhere else.")
        except ValueError:
            print("Remember, positions on the field are given by a row from A-J and a column from 1-10.")

        return False

    def place(self):
        """Place a ship on the board."""

        # Loop through all the ships
        for ship in Ships:
            print(f"Placing: {ship.name}")
            length = 0
            
            match ship:
                case Ships.CARRIER:
                    length = 5
                case Ships.BATTLESHIP:
                    length = 4
                case Ships.CRUISER:
                    length = 3
                case Ships.SUBMARINE:
                    length = 3
                case _:
                    length = 2

            position = self.validate_position(input("Enter a position (eg. A1): "))
            while not position:
                position = self.validate_position(input("Enter a position (eg. A1): "))

            print(position)
            

            

            direction = input("")
            

    def serialize(self) -> str:
        """Convert the game state into a string."""

        state = ""
        for i in self.board:
            for j in i:
                pass

        return state