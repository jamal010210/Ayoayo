import math
import random

from game_logic.Player import Player

# pylint: disable=too-few-public-methods
# Start with four beans per field
INITIAL_BEAN_COUNT = 4

class Field:
    """Field owns beans"""

    def __init__(self, owner: Player):
        self.owner = owner
        self.bean_positions = []
        for _ in range(0, INITIAL_BEAN_COUNT):
            self.add_bean()

    def clone(self):
        """Make a copy of this field."""
        clone = Field(self.owner)
        clone.bean_positions = self.bean_positions.copy()
        return clone
    
    def add_bean(self):
        """Adds a bean to this field by calculating a random position where it should appear within the circle."""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, 0.8)
        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)
        self.bean_positions.append((dx, dy))
        
    def bean_count(self):
        """Returns the current amount of beans this field holds."""
        return len(self.bean_positions)
        
        
    def remove_beans(self):
        """Clears all the beans currently in this field."""
        previous_bean_count = self.bean_count()
        self.bean_positions = []
        return previous_bean_count
        
