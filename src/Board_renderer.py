import pygame


class Renderer:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    HOLE_RADIUS = 40
    BACKGROUND_COLOR = (139, 90, 43)   # brown wood color
    HOLE_COLOR = (80, 40, 10)
    BEAN_COLOR = (240, 220, 130)
    TEXT_COLOR = (255, 255, 255)
    
    
    def __init__(self, board):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Ayo Game")
        self.board = board
        self.font = pygame.font.SysFont(None, 36)
        self.hole_positions = [] 
        self.build_hole_position()
        

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self._draw_fields()
        pygame.display.flip()
        
    def build_hole_position(self):
        fields = self.board.field_collection.fields
        half = len(fields) // 2

        for i in range(half):
            # bottom row (player 1, fields 0-5)
            x = 100 + i * 110
            y = 300
            self.hole_positions.append((i, x, y))
            

            # top row (player 2, fields 6-11)
            x = 100 + (half - 1 - i) * 110  # reversed for player 2
            y = 100
            self.hole_positions.append((i + half, x, y))
            

    def _draw_fields(self):
        fields = self.board.field_collection.fields

        for field_index, x, y in self.hole_positions:
            self._draw_hole(x, y, fields[field_index].beans)

           
            

    def _draw_hole(self, x, y, bean_count):
            pygame.draw.circle(self.screen, self.HOLE_COLOR, (x, y), self.HOLE_RADIUS)
            text = self.font.render(str(bean_count), True, self.TEXT_COLOR)
            self.screen.blit(text, (x - 10, y - 10))
        