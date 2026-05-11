from game_logic.Player import Player


# pylint: disable=too-few-public-methods

class Field:
    '''Field owns four beans'''
    INITIAL_BEAN_COUNT = 4

    def __init__(self, owner: Player):
        self.owner = owner
        self.beans = Field.INITIAL_BEAN_COUNT
        self.bean_positions = []

    def clone(self):
        '''Make a copy of this field'''
        clone = Field(self.owner)
        clone.beans = self.beans
        clone.bean_positions = self.bean_positions
        return clone
