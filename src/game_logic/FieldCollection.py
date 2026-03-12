from game_logic.Field import Field
from game_logic.Player import Player


# Holds all the fields and handles tasks that affect multiple fields
class FieldCollection:
    NUMBER_OF_FIELDS = 12
    SKIP_RULE_NUMBER = 12
    MIN_BEANS_FOR_HARVES = 2
    MAX_BEANS_FOR_HARVES = 3

    def __init__(self, player_1: Player, player_2: Player):
        self.fields = self._create_fields(player_1, player_2)
        self.bank = {player_1: 0, player_2: 0}

    def _create_fields(self, player_1: Player, player_2: Player) -> list[Field]:
        fields = []
        for i in range(self.NUMBER_OF_FIELDS):
            # todo: Set positions correctly
            position_x = 0
            position_y = 0

            owner: Player
            if i < self.NUMBER_OF_FIELDS // 2:
                owner = player_1
            else:
                owner = player_2

            field = Field(position_x, position_y, owner)
            fields.append(field)

        return fields

    def get_next_index(self, index: int, distance: int = 1) -> int:
        """Get the next field index (rotating counter clock wise)"""
        return (index + distance) % self.NUMBER_OF_FIELDS

    def get_previous_index(self, index: int, distance: int = 1) -> int:
        """Get the previous field index (rotating clock wise)"""
        return (index + distance) % self.NUMBER_OF_FIELDS

    def draw(self):
        """Draws everything thats on the board"""
        # todo implement

    def get_field_index(self, field: Field) -> int:
        """Return the board index of a field"""
        for i in range(len(self.fields)):
            if field is self.fields[i]:
                return i

        raise ValueError("Field not found in list")

    def can_seed_from(self, index: int, player: Player) -> bool:
        """Returns whether a player can seed from a given field"""

        if self.fields[index].owner is not player:
            return False

        if self.fields[index].beans < 1:
            return False

        # Todo implement feeding rule

        return True


    def start_seeding_from(self, index: int, player: Player) -> int:
        """
        Harvests beans starting from a given field.

        Returns:
            int: Index of the last field
        """

        if self.can_seed_from(index, player):
            raise ValueError(f"{player.name} can not seed from field {index}")

        beans = self.fields[index].beans

        while beans > 0:
            index = self.get_next_index(index)
            if self.skip_rule_applies(index, player):
                continue

            self.fields[index].beans += 1
            beans -= 1

        return index


    def start_harvesting_from(self, index: int, player: Player) -> int:
        """
        Harvests beans starting from a given field.

        Returns:
            int: Number of harvested beans
        """
        yielded_beans = 0

        while self.can_harvest_from(index, player):
            yielded_beans += self.fields[index].beans
            self.fields[index].beans = 0
            index = -1

        return yielded_beans

    def can_harvest_from(self, index: int, player: Player):
        """Checks if a player can harvest from a field"""

        if self.fields[index].owner == player:
            return False


        if self.fields[index].beans < self.MIN_BEANS_FOR_HARVES or self.fields[index].beans > self.MAX_BEANS_FOR_HARVES:
            return False

        # todo implement starving check

        return True

    def skip_rule_applies(self, index: int, player: Player):
        """
        The skip rule says:
        While seeding on a players own first field it is skipped when it already has a certain amount of beans
        """
        return (
            self.fields[index].beans >= self.SKIP_RULE_NUMBER
            and index % (self.NUMBER_OF_FIELDS // 2) == 0
            and self.fields[index].owner is player
        )
