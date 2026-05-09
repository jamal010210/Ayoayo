from game_logic.Player import Player


class Field:
    INITIAL_BEAN_COUNT = 4

    def __init__(self, owner: Player):
        self.owner = owner
        self.beans = Field.INITIAL_BEAN_COUNT
        self.bean_positions = [] 

    def clone(self):
        clone = Field(self.position_x, self.position_y, self.owner)
        clone.beans = self.beans
        clone.bean_positions = self.bean_positions
        return clone
