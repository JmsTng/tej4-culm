from enum import Enum
from getkey import getkey, keys
from text import Console


class Ships(Enum):
    """Collect ship types in an enumerable."""

    CARRIER = 1
    BATTLESHIP = 2
    CRUISER = 3
    SUBMARINE = 4
    DESTROYER = 5


class Battleship:
    MISS = 8
    HIT = 9

    def __init__(self, rows: int = 10, cols: int = 10):
        self.ROWS = rows
        self.COLS = cols
        self.board_self = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.board_oppo = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.ships_alive = 0

    def check_bounds(self, coords: tuple[int, int]) -> bool:
        """Evaluate if coordinates fall within the board boundaries."""

        return 0 <= coords[0] < self.ROWS and 0 <= coords[1] < self.COLS

    def get_coords(self, position: str) -> tuple[int, int]:
        """Return the ordered pair for a valid coordinate string."""

        try:
            # Split string into row and column components
            row = position[0]
            col = position[1:]

            # Calculate list indices
            row = ord(row.upper()) - ord("A")
            col = int(col) - 1

            if self.check_bounds((row, col)):
                return (row, col)
        except (ValueError, IndexError):
            print("Remember, positions on the field are given by a row from A-J and a column from 1-10.")

        return (-1, -1)

    def get_value(self, coords: tuple[int, int], oppo: bool = False) -> int:
        """Returns the value at a given coordinate."""
        
        return self.board_oppo[coords[0]][coords[1]] if oppo else self.board_self[coords[0]][coords[1]]

    def find(self, value: int, oppo: bool = False) -> bool:
        """Return whether a value is present on the board."""

        board = self.board_oppo if oppo else self.board_self
        return any([value in row for row in board])

    def validate_position(self, position: str | None = None, coords: tuple[int, int] = (-1, -1)) -> bool | tuple[int, int]:
        """Check that a given position is within board boundaries."""

        # Used to catch errors if the position is not properly formatted.
        try:
            if position is not None:
                row, col = self.get_coords(position)

                if row == -1 or col == -1:
                    print("That's not in our patrol range, commander! Let's focus somewhere else.")
                    return False
            else:
                row, col = coords

                if not self.check_bounds((row, col)):
                    print("That's not in our patrol range, commander! Let's focus somewhere else.")
                    return False

            # Check that the cell is not occupied
            if self.board_self[row][col]:
                print("That spot is occupied!")
                return False
                
            return (row, col)  # If valid, return the position
        except (ValueError, IndexError):  # If invalid because position is malformed
            print("Remember, positions on the field are given by a row from A-J and a column from 1-10.")

        # Return False
        return False

    def place_easy(self):
        """Diagnostic tool to quickly set up a board."""

        self.board_self = [
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
            [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 4, 0, 0, 0, 0, 0, 0, 0],
            [5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.ships_alive = 5

    def place(self) -> None:
        """Place the ships on the board."""

        # Loop through all the ships
        for ship in Ships:
            Console.clear()

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
        
        self.ships_alive = 5

    def place_ship(self, ship: Ships, length: int, char: str = ""):
        """Handle the placing of a single ship."""

        print(f"Placing: {Console.BWHITE}{ship.name}{Console.RESET}")
        print(self.pretty_print())

        # Ask for and validate the positioning of a ship.
        position = self.validate_position(input("Enter a position (eg. A1): "))
        while not position:
            Console.clear(1)
            print(self.pretty_print())
            position = self.validate_position(input("Enter a position (eg. A1): "))

        row, col = position[0], position[1]

        k = None
        positions = []
        past_positions = []
        valid = False

        while k != keys.ENTER or not valid or not past_positions:
            if not valid:
                print("Use the arrow keys to control the direction!")

            # Get direction input
            k = getkey()
            Console.clear()

            # Identify valid orientations
            if k == keys.UP and row - (length - 1) >= 0:
                positions = [(row - i, col) for i in range(length)]
                valid = True
            elif k == keys.DOWN and row + (length - 1) <= self.ROWS:
                positions = [(row + i, col) for i in range(length)]
                valid = True
            elif k == keys.LEFT and col - (length - 1) >= 0:
                positions = [(row, col - i) for i in range(length)]
                valid = True
            elif k == keys.RIGHT and col + (length - 1) <= self.COLS:
                positions = [(row, col + i) for i in range(length)]
                valid = True
            elif k == keys.ENTER:
                # Done to ensure pressing ENTER does not violate the loop condition
                valid = True
            else:
                valid = False

            # Check for collisions along the ship path
            if any([False if self.validate_position(coords=pos) else True for pos in positions]):
                valid = False
                positions = past_positions

            print(f"Placing: {Console.BWHITE}{ship.name}{Console.RESET} @ ({chr(row + ord('A'))}{col + 1})")
            print(self.pretty_print(positions, char))

            past_positions = positions

        for row, col in positions:
            self.board_self[row][col] = ship.value

    def serialize(self) -> str:
        """Convert the game state into a string."""

        self_state = ""
        oppo_state = ""

        # Collapse both boards into a representative string
        for i in self.board_self:
            for j in i:
                self_state += str(j)

        for i in self.board_oppo:
            for j in i:
                oppo_state += str(j)

        return self_state + oppo_state

    def pretty_print(self, positions: list[tuple[int, int]] = [], char: str = "", colour: str = Console.BYELLOW) -> str:
        """Output the board with optional temporary modifications."""

        _ = []

        for i, row in enumerate(self.board_self):
            line = [chr(ord("A") + i)] # Row identifier

            # Loop through each cell in the board
            for col in row:
                # Change what is output depending on cell value
                if col == 0:
                    line.append(Console.BLUE + "~")
                elif col == Ships.CARRIER.value:
                    line.append(Console.BYELLOW + "▨")
                elif col == Ships.BATTLESHIP.value:
                    line.append(Console.BYELLOW + "▩")
                elif col == Ships.CRUISER.value:
                    line.append(Console.BYELLOW + "▥")
                elif col == Ships.SUBMARINE.value:
                    line.append(Console.BYELLOW + "▢")
                elif col == Ships.DESTROYER.value:
                    line.append(Console.BYELLOW + "▣")
                elif col == self.MISS:
                    line.append(Console.GREY + "⋅")
                elif col == self.HIT:
                    line.append(Console.BRED + "+")

            line.append(Console.RESET)
            _.append(line)

        # Overwrite positions with custom data for ephemeral display
        if positions:
            for row, col in positions:
                _[row][col + 1] = colour + char

        _.insert(0, ["  1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

        return "\n".join([" ".join(row) for row in _])
