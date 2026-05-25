import math
import pygame
from Board_renderer import Renderer, HOLE_RADIUS
from game_logic.Game import Game
import persistence
from bot.bot_logic import choose_move
from GameMode import GameMode
from GameSession import GameSession
from HistoryController import HistoryController
# pylint: disable=no-member


pygame.init()
persistence.init_db()
class App:
    """
    Main application controller for the Ayoayo game.

    Responsible for:
    - Initializing core game components (Game, Renderer, History, Session)
    - Managing the game loop execution (events, updates, rendering)
    - Maintaining runtime state such as clock and UI-related flags
    """
    def __init__(self):
        self.game = Game()
        self.session = GameSession(self.game)
        self.renderer = Renderer(self.game)
        self.history = HistoryController(self.renderer, persistence)
        self.clock = pygame.time.Clock()

        self.bot_search_depth = None
        self.names_set = False

    def run(self):
        """runs game loop"""
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event.pos)

            if event.type == pygame.KEYDOWN:
                self.handle_key(event)


    def handle_mouse(self, pos):
        """Handle all mouse click input."""
        if self.history.active:
            self.history.handle_click(pos)
            return

        if self.game.mode is None:
            self.handle_menu_click(pos)
            return

        if self.game.mode == GameMode.HUMAN_VS_BOT and self.bot_search_depth is None:
            self.bot_search_depth = (
                self.renderer.get_depth_from_position(pos)
                or self.bot_search_depth
            )
            return

        if not self.names_set:
            self.renderer.handle_name_input_click(pos, self.game.mode)
            return

        if self.renderer.get_return_to_menu_button_collision(pos):
            self.reset_game()
            return

        if self.renderer.get_undo_button_collision(pos):
            self.game.undo_turn()
            return

        self.handle_board_click(pos)


    def handle_key(self, event):
        """Handle keyboard input."""

        if self.history.active:
            self.history.handle_key(event)
            return

        if not self.names_set:
            if self.renderer.handle_name_input_key(event, self.game.mode):
                player1_name, player2_name = self.renderer.get_player_names()

                if self.game.mode == GameMode.HUMAN_VS_HUMAN:
                    self.game.set_player_names(player1_name, player2_name)
                else:
                    self.game.set_player_names(player1_name, "Bot")

                self.names_set = True


    def handle_menu_click(self, pos):
        """Handle clicks on the main menu."""
        selected_mode = self.renderer.get_mode_from_position(pos)
        if selected_mode is not None:
            self.game.mode = selected_mode
            return

        if self.renderer.get_history_button_collision(pos):
            self.history.open()


    def handle_board_click(self, pos):
        """Handle clicks on the game board."""
        click_x, click_y = pos

        for field_index, x, y in self.renderer.hole_positions:
            distance = math.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)

            if distance < HOLE_RADIUS:
                try:
                    self.game.board.seed_from_field(field_index, self.game.current_player())
                    self.game.end_turn()
                except ValueError:
                    pass


    def update(self):
        """Update game state each frame."""
        self.handle_bot_move()
        self.session.save_result()


    def handle_bot_move(self):
        """Let bot make a move if it is its turn."""
        if self.game.mode != GameMode.HUMAN_VS_BOT:
            return

        if self.game.current_player() != self.game.player_2:
            return

        move = choose_move(
            self.game.board,
            self.game.current_player(),
            self.bot_search_depth if self.bot_search_depth else 1,
        )

        if move is not None:
            self.game.board.seed_from_field(move, self.game.current_player())
            self.game.end_turn()


    def reset_game(self):
        """Reset the current game state."""

        self.game = Game()
        self.renderer.game = self.game

        self.session = GameSession(self.game)
        self.bot_search_depth = None
        self.names_set = False

        self.history.close()


    def render(self):
        """Render the current frame."""
        if self.game.mode is None:
            if self.history.active:
                self.history.render()
            else:
                self.renderer.draw_mode_selection()

        elif self.game.mode == GameMode.HUMAN_VS_BOT and self.bot_search_depth is None:
            self.renderer.draw_depth_selection()

        elif not self.names_set:
            self.renderer.draw_name_input(self.game.mode)

        else:
            self.renderer.draw()


if __name__ == "__main__":
    pygame.init()
    persistence.init_db()
    App().run()
