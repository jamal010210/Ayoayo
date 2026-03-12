from typing import Self
from game_logic.FieldCollection import FieldCollection
from game_logic.Player import Player


class Board:
    """
    The board. Contains the fields and the banks.
    Can be used as a state to undo turns.
    """

    def __init__(self, player_1: Player, player_2: Player):
        self.beans_player_1 = 0
        self.beans_player_2 = 0
        self.field_collection = FieldCollection(player_1, player_2)

    def clone_deep(self) -> Self:
        raise NotImplementedError  # todo implement

    def draw(self):
        """Draw the entire board."""
        raise NotImplementedError  # todo implement
