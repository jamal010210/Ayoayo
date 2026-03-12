from typing import Self
from game_logic.FieldCollection import FieldCollection
from game_logic.Player import Player


class Board:
    """
    The board. Contains the fields and the banks.
    Can be used as a state to undo turns.
    """

    def __init__(self, player_1: Player, player_2: Player):
        self.bank = {player_1: 0, player_2: 0}
        self.field_collection = FieldCollection(player_1, player_2)

    def seed_from_field(self, index: int, player: Player):
        last_field = self.field_collection.start_seeding_from(index, player)
        harvested_beans = self.field_collection.start_harvesting_from(last_field, player)
        self.bank[player] += harvested_beans

    def clone_deep(self) -> Self:
        raise NotImplementedError  # todo implement

    def draw(self):
        """Draw the entire board."""
        self.field_collection.draw()

        # todo: remove this console output code
        for player in self.bank:
            print(f"{player.name}: {self.bank[player]}")

        # todo: Draw board related stuff (E.g. bank)
