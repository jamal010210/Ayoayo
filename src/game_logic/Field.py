from game_logic.Player import Player


class Field:
    INITIAL_BEAN_COUNT = 4

    def __init__(self, position_x: int, position_y: int, owner: Player):
        self.position_x = position_x
        self.position_y = position_y
        self.owner = owner
        self.beans = Field.INITIAL_BEAN_COUNT
