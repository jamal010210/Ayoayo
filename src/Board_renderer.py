import random
import math
import pygame

# pylint: disable=no-member

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
HOLE_RADIUS = 90
BACKGROUND_COLOR = (39, 35, 24)  # brown wood color
BEAN_COLOR = (240, 220, 130)
TEXT_COLOR = (255, 255, 255)
BEAN_SIZE = 20




class Renderer:
    """Renders the game board, holes, beans and win screen using pygame."""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ayo Game")
        self.game = game
        self.board = game.board
        self.font = pygame.font.SysFont(None, 36)
        self.hole_image = pygame.image.load("img/hole.png")  # load assets first
        self.bean_image = pygame.image.load("img/bean.png")
        self.player1_wins_image = pygame.image.load("img/player_one_wins.png")
        self.player2_wins_image = pygame.image.load("img/player_two_wins.png")
        self.draw_image = pygame.image.load("img/draw.png")
        self.bean_image = pygame.transform.scale(
            self.bean_image, (BEAN_SIZE * 2, BEAN_SIZE * 2)
        )
        self.hole_image = pygame.transform.scale(
            self.hole_image, (HOLE_RADIUS * 2, HOLE_RADIUS * 2)
        )
        self.hole_positions = []
        self.build_hole_position()
        self.mode_buttons = self._build_mode_buttons()

    def draw(self):
        """Draws the current game state on screen."""
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_fields()
        self.draw_scores()
        if self.game.winner:
            self.draw_winner(self.game.winner)
        pygame.display.flip()

    def _build_mode_buttons(self) -> dict[str, pygame.Rect]:
        button_width = 400
        button_height = 90
        gap = 40
        total_width = button_width * 2 + gap
        x_start = (WINDOW_WIDTH - total_width) // 2
        y_start = WINDOW_HEIGHT // 2 - button_height // 2

        return {
            "1": pygame.Rect(x_start, y_start, button_width, button_height),
            "2": pygame.Rect(x_start + button_width + gap, y_start, button_width, button_height),
        }

    def draw_mode_selection(self):
        """Draws the mode selection screen with two buttons."""
        self.screen.fill(BACKGROUND_COLOR)
        title_text = self.font.render("Choose mode:", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        for mode_key, rect in self.mode_buttons.items():
            pygame.draw.rect(self.screen, (80, 80, 80), rect)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, 4)
            label = (
                "Human vs Human"
                if mode_key == "1"
                else "Human vs Bot"
            )
            label_text = self.font.render(label, True, TEXT_COLOR)
            label_rect = label_text.get_rect(center=rect.center)
            self.screen.blit(label_text, label_rect)

        pygame.display.flip()

    def get_mode_from_position(self, position: tuple[int, int]) -> str | None:
        """Returns the selected mode key for a click position."""
        for mode_key, rect in self.mode_buttons.items():
            if rect.collidepoint(position):
                return mode_key
        return None

    def build_hole_position(self):
        """Calculates and stores the screen positions of all holes."""
        fields = self.board.field_collection.fields
        half = len(fields) // 2

        for i in range(half):
            # bottom row (player 1, fields 0-5)
            x = 100 + i * 250
            y = 600
            self.hole_positions.append((i, x, y))

            # top row (player 2, fields 6-11)
            x = 100 + (half - 1 - i) * 250  # reversed for player 2
            y = 200
            self.hole_positions.append((i + half, x, y))

    def update_bean_positions(self):
        """Randomizes bean positions within each hole after a move."""
        fields = self.board.field_collection.fields
        for field_index, x, y in self.hole_positions:
            field = fields[field_index]
            field.bean_positions = []
            for _ in range(field.beans):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0, HOLE_RADIUS - BEAN_SIZE)
                bx = x + distance * math.cos(angle)
                by = y + distance * math.sin(angle)
                field.bean_positions.append((bx, by))

    def _draw_fields(self):
        """Draws all holes and their beans on the screen."""
        fields = self.board.field_collection.fields
        for field_index, x, y in self.hole_positions:
            self._draw_hole(x, y, fields[field_index])

    def _draw_hole(self, x, y, field):
        """Draws a single hole image and its beans at the given position."""
        self.screen.blit(self.hole_image, (x - HOLE_RADIUS, y - HOLE_RADIUS))
        for bx, by in field.bean_positions:
            self.screen.blit(
                self.bean_image, (int(bx) - BEAN_SIZE, int(by) - BEAN_SIZE)
            )

    def draw_winner(self, winner):
        """Displays each player's current bean count on screen."""
        image = None
        if winner == "draw":
            image = self.draw_image
        elif winner == self.game.player_1:
            image = self.player1_wins_image
        elif winner == self.game.player_2:
            image = self.player2_wins_image
        if image:  # ← only blit if image was actually assigned
            x = (WINDOW_WIDTH - image.get_width()) // 2
            y = (WINDOW_HEIGHT - image.get_height()) // 2
            self.screen.blit(image, (x, y))

    def draw_scores(self):
        """Displays each player's current bean count on screen."""
        score_p1 = self.board.bank[self.game.player_1]
        score_p2 = self.board.bank[self.game.player_2]

        text_p1 = self.font.render(f"Player 1: {score_p1}", True, TEXT_COLOR)
        text_p2 = self.font.render(f"Player 2: {score_p2}", True, TEXT_COLOR)

        self.screen.blit(text_p1, (50, 20))
        self.screen.blit(text_p2, (50, 50))
