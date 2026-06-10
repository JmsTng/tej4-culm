from enum import Enum
from getkey import getkey, keys
from text import Colours
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

    def validate_position(self, position: str | None = None, coords: tuple[int, int] = (-1, -1)) -> Literal[False] | tuple[int, int]:
        """Check that a given position is within board boundaries."""

        # Used to catch errors if the position is not properly formatted.
        try:
            row, col = coords
            
            if position is not None:
                # Only use the first two characters
                row = position[0]
                col = position[1:]

                # Calculate list indices
                row = ord(row.upper()) - ord("A")
                col = int(col) - 1

            # Check that the cell exists and is not occupied
            if 0 <= row < self.ROWS and 0 <= col < self.COLS:
                if self.board_self[row][col]:
                    print("That spot is occupied!")
                    return False
                return (row, col) # If valid, return the position
            print("That's not in our patrol range, commander! Let's focus somewhere else.")
        except (ValueError, IndexError): # If invalid because position is malformed
            print("Remember, positions on the field are given by a row from A-J and a column from 1-10.")

        # Return False
        return False

    def place(self):
        """Place the ships on the board."""

        # Loop through all the ships
        for ship in Ships:
            print(f"Placing: {Colours.BWHITE}{ship.name}{Colours.RESET}")

            # Place each ship
            match ship:
                case Ships.CARRIER:
                    self.place_ship(Ships.CARRIER, 5, "▨")
                case Ships.BATTLESHIP:
                    self.place_ship(Ships.BATTLESHIP, 4, "▩")
                case Ships.CRUISER:
                    self.place_ship(Ships.CRUISER, 3, "▥")
                case Ships.SUBMARINE:
                    self.place_ship(Ships.SUBMARINE, 3, "▢")
                case _:
                    self.place_ship(Ships.DESTROYER, 2, "▣")

    def place_ship(self, ship: Ships, length: int, char: str = ""):
        """Handle the placing of a single ship."""

        # Ask for and validate the positioning of a ship.
        position = self.validate_position(input("Enter a position (eg. A1): "))
        while not position:
            position = self.validate_position(input("Enter a position (eg. A1): "))

        row, col = position[0], position[1]
        
        k = None
        positions = []
        past_positions = []
        valid = False
        while k != keys.ENTER or not valid:
            k = getkey()

            # Diagnostic prints
            # print(f"length: {length}")
            # print(f"up: {row - (length - 1)}")
            # print(f"down: {row + (length - 1)}")
            # print(f"left: {col - (length - 1)}")
            # print(f"right: {col + (length - 1)}")
            
            if row - (length - 1) >= 0 and k == keys.UP:
                positions = [(row - i, col) for i in range(length)]
                valid = True
            elif row + (length - 1) <= self.ROWS and k == keys.DOWN:
                positions = [(row + i, col) for i in range(length)]
                valid = True
            elif col - (length - 1) >= 0 and k == keys.LEFT:
                positions = [(row, col - i) for i in range(length)]
                valid = True
            elif col + (length - 1) <= self.COLS and k == keys.RIGHT:
                positions = [(row, col + i) for i in range(length)]
                valid = True
            elif k == keys.ENTER:
                valid = True
            else:
                valid = False

            if any([False if self.validate_position(coords=pos) else True for pos in positions]):
                valid = False
                positions = past_positions

            print(self.pretty_print(positions, char))
            print()
            print()

            past_positions = positions

        for row, col in positions:
            self.board_self[row][col] = ship.value

        # direction = input("")

    def serialize(self) -> str:
        """Convert the game state into a string."""

        state = ""
        for i in self.board_self:
            for j in i:
                ...

        return state

    def pretty_print(self, positions: list[tuple[int, int]] = [], char: str = "", colour: str = Colours.BYELLOW) -> str:
        _ = []
        
        for row in self.board_self:
            line = []
            
            for col in row:
                if col == 0:
                    line.append(Colours.BLUE + "~")
                elif col == Ships.CARRIER.value:
                    line.append(Colours.BYELLOW + "▨")
                elif col == Ships.BATTLESHIP.value:
                    line.append(Colours.BYELLOW + "▩")
                elif col == Ships.CRUISER.value:
                    line.append(Colours.BYELLOW + "▥")
                elif col == Ships.SUBMARINE.value:
                    line.append(Colours.BYELLOW + "▢")
                elif col == Ships.DESTROYER.value:
                    line.append(Colours.BYELLOW + "▣")
                elif col == 8: # Miss
                    line.append(Colours.GREY + "⋅")
                elif col == 9: # Hit
                    line.append(Colours.BRED + "+")
                    
            line.append(Colours.RESET)
            _.append(line)

        if positions:
            for row, col in positions:
                _[row][col] = colour + char
        
        return "\n".join(["".join(row) for row in _])


bs = Battleship()
bs.place()