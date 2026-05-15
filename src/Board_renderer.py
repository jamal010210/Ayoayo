import pygame

from GameMode import GameMode
from game_logic.Game import Game

# pylint: disable=no-member

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
HOLE_RADIUS = 90
TOP_ROW_Y = 200
BOTTOM_ROW_Y = 520
FIELD_COUNT_LABEL_OFFSET = 36
BACKGROUND_COLOR = (39, 35, 24)  # brown wood color
BEAN_COLOR = (240, 220, 130)
TEXT_COLOR = (255, 255, 255)
BEAN_RADIUS = 20
BUTTON_FILL_COLOR = (80, 80, 80)
UNDO_BUTTON_WIDTH = 180
UNDO_BUTTON_HEIGHT = 70
UNDO_BUTTON_MARGIN = 30
RETURN_BUTTON_WIDTH = 280
RETURN_BUTTON_HEIGHT = 70
RETURN_BUTTON_MARGIN = 30
MODE_BUTTON_LABELS: dict[GameMode, str] = {
    GameMode.HUMAN_VS_HUMAN: "Human vs Human",
    GameMode.HUMAN_VS_BOT: "Human vs Bot",
}


class Renderer:
    """Renders the game board, holes, beans and win screen using pygame."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, game: Game):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ayo Game")
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        self.hole_image = pygame.image.load("img/hole.png")  # load assets first
        self.bean_image = pygame.image.load("img/bean.png")
        self.player1_wins_image = pygame.image.load("img/player_one_wins.png")
        self.player2_wins_image = pygame.image.load("img/player_two_wins.png")
        self.draw_image = pygame.image.load("img/draw.png")
        self.bean_image = pygame.transform.scale(
            self.bean_image, (BEAN_RADIUS * 2, BEAN_RADIUS * 2)
        )
        self.hole_image = pygame.transform.scale(
            self.hole_image, (HOLE_RADIUS * 2, HOLE_RADIUS * 2)
        )
        self.hole_positions = []
        self.build_hole_position()
        self.mode_buttons = self._build_mode_buttons()
        self.depth_buttons = self._build_depth_buttons()
        self.name_input_fields = {}
        self.player_names = {}
        self.active_field = None
        self._build_name_input_fields()
        self.undo_button = self._build_undo_button()
        self.return_to_menu_button = self._build_return_to_menu_button()

    def draw(self):
        """Draws the current game state on screen."""
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_fields()
        self.draw_scores()
        self.draw_return_to_menu_button()
        if self.game.mode == GameMode.HUMAN_VS_HUMAN:
            self.draw_undo_button()
        if self.game.winner:
            self.draw_winner(self.game.winner)
        pygame.display.flip()

    def _build_mode_buttons(self) -> dict[GameMode, pygame.Rect]:
        button_width = 400
        button_height = 90
        gap = 40
        total_width = button_width * 2 + gap
        x_start = (WINDOW_WIDTH - total_width) // 2
        y_start = WINDOW_HEIGHT // 2 - button_height // 2

        return {
            GameMode.HUMAN_VS_HUMAN: pygame.Rect(
                x_start, y_start, button_width, button_height
            ),
            GameMode.HUMAN_VS_BOT: pygame.Rect(
                x_start + button_width + gap,
                y_start,
                button_width,
                button_height,
            ),
        }

    def draw_mode_selection(self):
        """Draws the mode selection screen with two buttons."""
        self.screen.fill(BACKGROUND_COLOR)
        title_text = self.font.render("Choose mode:", True, TEXT_COLOR)
        title_rect = title_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        )
        self.screen.blit(title_text, title_rect)

        for mode_key, rect in self.mode_buttons.items():
            pygame.draw.rect(self.screen, (80, 80, 80), rect)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, 4)
            label = MODE_BUTTON_LABELS[mode_key]
            label_text = self.font.render(label, True, TEXT_COLOR)
            label_rect = label_text.get_rect(center=rect.center)
            self.screen.blit(label_text, label_rect)

        pygame.display.flip()

    def get_mode_from_position(
        self, position: tuple[int, int]
    ) -> GameMode | None:
        """Returns the selected mode key for a click position."""
        for mode_key, rect in self.mode_buttons.items():
            if rect.collidepoint(position):
                return mode_key
        return None

    def _build_depth_buttons(self) -> dict[int, pygame.Rect]:
        button_width = 280
        button_height = 90
        gap = 30
        total_width = button_width * 3 + gap * 2
        x_start = (WINDOW_WIDTH - total_width) // 2
        y_start = WINDOW_HEIGHT // 2 - button_height // 2

        return {
            1: pygame.Rect(x_start, y_start, button_width, button_height),
            2: pygame.Rect(
                x_start + button_width + gap,
                y_start,
                button_width,
                button_height,
            ),
            3: pygame.Rect(
                x_start + (button_width + gap) * 2,
                y_start,
                button_width,
                button_height,
            ),
        }

    def draw_depth_selection(self):
        """Draws the depth selection screen with three buttons."""
        self.screen.fill(BACKGROUND_COLOR)
        title_text = self.font.render("Choose difficulty:", True, TEXT_COLOR)
        title_rect = title_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        )
        self.screen.blit(title_text, title_rect)

        depth_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
        for depth_key, rect in self.depth_buttons.items():
            pygame.draw.rect(self.screen, (80, 80, 80), rect)
            pygame.draw.rect(self.screen, TEXT_COLOR, rect, 4)
            label_text = self.font.render(
                depth_labels[depth_key], True, TEXT_COLOR
            )
            label_rect = label_text.get_rect(center=rect.center)
            self.screen.blit(label_text, label_rect)

        pygame.display.flip()

    def get_depth_from_position(self, position: tuple[int, int]) -> int | None:
        """Returns the selected depth key for a click position."""
        for depth_key, rect in self.depth_buttons.items():
            if rect.collidepoint(position):
                return depth_key
        return None

    def _build_undo_button(self) -> pygame.Rect:
        return pygame.Rect(
            WINDOW_WIDTH - UNDO_BUTTON_WIDTH - UNDO_BUTTON_MARGIN,
            WINDOW_HEIGHT - UNDO_BUTTON_HEIGHT - UNDO_BUTTON_MARGIN,
            UNDO_BUTTON_WIDTH,
            UNDO_BUTTON_HEIGHT,
        )

    def get_undo_button_collision(self, position: tuple[int, int]) -> bool:
        """Returns whether a click position is inside the undo button."""
        return self.undo_button.collidepoint(position)

    def _build_return_to_menu_button(self) -> pygame.Rect:
        return pygame.Rect(
            RETURN_BUTTON_MARGIN,
            WINDOW_HEIGHT - RETURN_BUTTON_HEIGHT - RETURN_BUTTON_MARGIN,
            RETURN_BUTTON_WIDTH,
            RETURN_BUTTON_HEIGHT,
        )

    def get_return_to_menu_button_collision(self, position: tuple[int, int]) -> bool:
        """Returns whether a click position is inside the return-to-menu button."""
        return self.return_to_menu_button.collidepoint(position)

    def build_hole_position(self):
        """Calculates and stores the screen positions of all holes."""
        fields = self.game.board.field_collection.fields
        half = len(fields) // 2

        for i in range(half):
            # bottom row (player 1, fields 0-5)
            x = 100 + i * 250
            y = BOTTOM_ROW_Y
            self.hole_positions.append((i, x, y))

            # top row (player 2, fields 6-11)
            x = 100 + (half - 1 - i) * 250  # reversed for player 2
            y = TOP_ROW_Y
            self.hole_positions.append((i + half, x, y))


    def _draw_fields(self):
        """Draws all holes, their beans, and each field's bean count."""
        fields = self.game.board.field_collection.fields
        for field_index, x, y in self.hole_positions:
            field = fields[field_index]
            self._draw_hole(x, y, field)
            bean_count_text = self.font.render(str(field.bean_count()), True, TEXT_COLOR)
            bean_count_rect = bean_count_text.get_rect(
                center=(x, y + HOLE_RADIUS + FIELD_COUNT_LABEL_OFFSET)
            )
            self.screen.blit(bean_count_text, bean_count_rect)

    def _draw_hole(self, x, y, field):
        """Draws a single hole image and its beans at the given position."""
        self.screen.blit(self.hole_image, (x - HOLE_RADIUS, y - HOLE_RADIUS))
        for dx, dy in field.bean_positions:
            self.screen.blit(
                self.bean_image,
                int(x + HOLE_RADIUS * dx - BEAN_RADIUS), int(y + HOLE_RADIUS * dy - BEAN_RADIUS)
            )

    def draw_winner(self, winner):
        """Displays winner"""
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

    def draw_scores(self) -> None:
        """Displays player names, scores, and highlights the active player."""
        score_p1 = self.game.board.bank[self.game.player_1]
        score_p2 = self.game.board.bank[self.game.player_2]

        current_player = self.game.current_player()

        color_p1 = (
            (0, 255, 0) if current_player == self.game.player_1 else TEXT_COLOR
        )
        color_p2 = (
            (0, 255, 0) if current_player == self.game.player_2 else TEXT_COLOR
        )

        text_p1 = self.font.render(
            f"{self.game.player_1.name}: {score_p1}", True, color_p1
        )
        text_p2 = self.font.render(
            f"{self.game.player_2.name}: {score_p2}", True, color_p2
        )

        self.screen.blit(text_p2, (50, 20))
        self.screen.blit(text_p1, (50, 50))

    def draw_undo_button(self) -> None:
        """Draws the undo button in the bottom-right corner."""
        pygame.draw.rect(self.screen, BUTTON_FILL_COLOR, self.undo_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.undo_button, 3)
        undo_text = self.font.render("Undo", True, TEXT_COLOR)
        undo_text_rect = undo_text.get_rect(center=self.undo_button.center)
        self.screen.blit(undo_text, undo_text_rect)

    def draw_return_to_menu_button(self) -> None:
        """Draws the return-to-menu button in the bottom-left corner."""
        pygame.draw.rect(self.screen, BUTTON_FILL_COLOR, self.return_to_menu_button)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.return_to_menu_button, 3)
        button_text = self.font.render("Return to menu", True, TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=self.return_to_menu_button.center)
        self.screen.blit(button_text, button_text_rect)

    def _build_name_input_fields(self):
        """Builds input field rectangles for player names."""
        input_width, input_height, gap = 500, 60, 80
        x_center, y_start = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - input_height // 2
        self.name_input_fields = {
            "player1": pygame.Rect(x_center - input_width // 2, y_start - gap, input_width, input_height),
            "player2": pygame.Rect(x_center - input_width // 2, y_start + gap, input_width, input_height),
        }
        self.player_names = {"player1": "", "player2": ""}

    def _draw_name_field(self, field_key, label):
        """Draw a single name input field."""
        rect = self.name_input_fields[field_key]
        is_active = self.active_field == field_key
        
        label_text = self.font.render(label, True, TEXT_COLOR)
        self.screen.blit(label_text, (rect.left - 120, rect.top + 10))
        
        pygame.draw.rect(self.screen, (120, 120, 120) if is_active else (80, 80, 80), rect)
        pygame.draw.rect(self.screen, (200, 200, 100) if is_active else TEXT_COLOR, rect, 3)
        
        name_text = self.font.render(self.player_names[field_key], True, TEXT_COLOR)
        self.screen.blit(name_text, (rect.left + 10, rect.top + 12))

    def draw_name_input(self, mode: str):
        """Draws the name input screen for player names."""
        self.screen.fill(BACKGROUND_COLOR)
        
        title = "Enter Player Names:" if mode == "1" else "Enter Your Name:"
        title_text = self.font.render(title, True, TEXT_COLOR)
        self.screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)))
        
        self._draw_name_field("player1", "Player 1:")
        if mode == "1":
            self._draw_name_field("player2", "Player 2:")
        
        instr_font = pygame.font.SysFont(None, 28)
        instr_text = instr_font.render("Click a field to enter name, Press ENTER to confirm", True, (200, 200, 200))
        self.screen.blit(instr_text, instr_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80)))
        
        pygame.display.flip()

    def handle_name_input_click(self, position: tuple[int, int], mode: str) -> bool:
        """Handles mouse clicks on name input fields."""
        if self.name_input_fields["player1"].collidepoint(position):
            self.active_field = "player1"
        elif mode == "1" and self.name_input_fields["player2"].collidepoint(position):
            self.active_field = "player2"
        return False

    def handle_name_input_key(self, event, mode: str) -> bool:
        """Handles keyboard input for name fields."""
        if event.type != pygame.KEYDOWN or not self.active_field:
            return False
        
        if event.key == pygame.K_RETURN:
            if mode == "1":
                if self.active_field == "player1" and self.player_names["player1"]:
                    self.active_field = "player2"
                elif self.active_field == "player2" and self.player_names["player2"]:
                    return True
            else:
                return bool(self.player_names["player1"])
        elif event.key == pygame.K_BACKSPACE:
            self.player_names[self.active_field] = self.player_names[self.active_field][:-1]
        elif event.unicode.isprintable() and len(self.player_names[self.active_field]) < 20:
            self.player_names[self.active_field] += event.unicode
        return False

    def get_player_names(self) -> tuple[str, str]:
        """Returns the entered player names."""
        return (
            self.player_names["player1"].strip() or "Player 1",
            self.player_names["player2"].strip() or "Player 2"
        )