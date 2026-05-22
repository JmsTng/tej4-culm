from enum import Enum

class Ships(Enum):
    """Collect ship types in an enumerable."""

    CARRIER = 1
    BATTLESHIP = 2
    DESTROYER = 3
    SUBMARINE = 4
    PATROLLER = 5

class Battleship:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(10)]

    def serialize(self) -> str:
        """Convert the game state into a string."""

        state = ""
        for i in self.board:
            for j in i:
                pass

        return state