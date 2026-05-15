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

    def _create_fields(self, player_1: Player, player_2: Player) -> list[Field]:
        fields = []
        for i in range(self.NUMBER_OF_FIELDS):

            owner: Player
            if i < self.NUMBER_OF_FIELDS // 2:
                owner = player_1
            else:
                owner = player_2

            field = Field(owner)
            fields.append(field)

        return fields

    def clone(self):
        # Create empty object instead of using the initializer unnecessarily
        clone = object.__new__(type(self))

        cloned_fields = []
        for field in self.fields:
            cloned_fields.append(field.clone())

        clone.fields = cloned_fields

        return clone

    def get_next_index(self, index: int, distance: int = 1):
        """Get the next field index (rotating counter clock wise)"""
        return (index + distance) % self.NUMBER_OF_FIELDS

    def get_previous_index(self, index: int, distance: int = 1):
        """Get the previous field index (rotating clock wise)"""
        return (index - distance) % self.NUMBER_OF_FIELDS

    def get_field_index(self, field: Field) -> int:
        """Return the board index of a field"""
        for i in range(len(self.fields)):
            if field is self.fields[i]:
                return i

        raise ValueError("Field not found in list")

    def opponent_has_no_beans(self, player: Player):
        """Returns true if the given player's opponent has no beans anymore."""

        for field in self.fields:
            if field.owner is not player:
                if field.bean_count() > 0:
                    return False
        return True

    def can_reach_opponent(self, index: int, player: Player):
        last_own_index = 0
        for i in range(self.NUMBER_OF_FIELDS):
            if self.fields[i].owner is player:
                last_own_index = i

        distance_to_opponent = (last_own_index - index) + 1
        return self.fields[index].bean_count() >= distance_to_opponent

    def has_valid_moves(self, player: Player):
        for i in range(self.NUMBER_OF_FIELDS):
            if self.can_seed_from(i, player):
                return True
        return False

    def can_seed_from(self, index: int, player: Player):
        """Returns whether a player can seed from a given field"""

        if self.fields[index].owner is not player:
            return False

        if self.fields[index].bean_count() < 1:
            return False


        # The feeding rule says:
        # When the opponent has no seeds, only let me take the seeds
        # from one of my field with which I can reach opponents field to feed him.

        if self.opponent_has_no_beans(player):
            if not self.can_reach_opponent(index, player):
                return False

        return True

    def start_seeding_from(self, index: int, player: Player):
        """
        Harvests beans starting from a given field.

        Returns:
            int: Index of the last field
        """

        if not self.can_seed_from(index, player):
            raise ValueError(f"{player.name} can not seed from field {index}")

        beans = self.fields[index].remove_beans()

        while beans > 0:
            index = self.get_next_index(index)
            if self.skip_rule_applies(index, player):
                continue

            self.fields[index].add_bean()
            beans -= 1

        return index

    def start_harvesting_from(self, index: int, player: Player):
        """
        Harvests beans starting from a given field.

        Returns:
            int: Number of harvested beans
        """
        yielded_beans = 0

        while self.can_harvest_from(index, player):
            yielded_beans += self.fields[index].remove_beans()
            index = self.get_previous_index(index)

        return yielded_beans

    def would_starve_opponent(self, index: int, player: Player):
        """If harvesting would leave opponent with no beans, you can not harvest"""
        total_opponent_beans = 0

        for field in self.fields:
            if field.owner is not player:
                total_opponent_beans += field.bean_count()

        return total_opponent_beans - self.fields[index].bean_count() == 0

    def can_harvest_from(self, index: int, player: Player):
        """Checks if a player can harvest from a field"""

        if self.fields[index].owner == player:
            return False

        if (
            self.fields[index].bean_count() < self.MIN_BEANS_FOR_HARVES
            or self.fields[index].bean_count() > self.MAX_BEANS_FOR_HARVES
        ):
            return False

        # todo implement starving check -done!
        if self.would_starve_opponent(index, player):
            return False

        return True

    def skip_rule_applies(self, index: int, player: Player):
        """
        The skip rule says:
        While seeding on a players own first field it is skipped when it already has a certain amount of beans
        """
        return (
            self.fields[index].bean_count() >= self.SKIP_RULE_NUMBER
            and index % (self.NUMBER_OF_FIELDS // 2) == 0
            and self.fields[index].owner is player
        )
