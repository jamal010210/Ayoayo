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
game = Game()
session = GameSession(game)
renderer = Renderer(game)
history = HistoryController(renderer, persistence)
clock = pygame.time.Clock()
bot_search_depth: int | None = None
names_set = False


def main():
    """Main game loop."""
    while True:
        handle_events()
        update()
        render()
        clock.tick(60)


def handle_events():
    """Process all pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse(event.pos)

        if event.type == pygame.KEYDOWN:
            handle_key(event)


def handle_mouse(pos):
    """Handle all mouse click input."""
    global bot_search_depth

    if history.active:
        history.handle_click(pos)
        return

    if game.mode is None:
        handle_menu_click(pos)
        return

    if game.mode == GameMode.HUMAN_VS_BOT and bot_search_depth is None:
        bot_search_depth = renderer.get_depth_from_position(pos) or bot_search_depth
        return

    if not names_set:
        renderer.handle_name_input_click(pos, game.mode)
        return

    if renderer.get_return_to_menu_button_collision(pos):
        reset_game()
        return

    if renderer.get_undo_button_collision(pos):
        game.undo_turn()
        return

    handle_board_click(pos)


def handle_key(event):
    """Handle keyboard input."""

    if history.active:
        history.handle_key(event)
        return

    if not names_set:
        if renderer.handle_name_input_key(event, game.mode):
            player1_name, player2_name = renderer.get_player_names()

            if game.mode == GameMode.HUMAN_VS_HUMAN:
                game.set_player_names(player1_name, player2_name)
            else:
                game.set_player_names(player1_name, "Bot")

            names_set = True


def handle_menu_click(pos):
    """Handle clicks on the main menu."""
    selected_mode = renderer.get_mode_from_position(pos)
    if selected_mode is not None:
        game.mode = selected_mode
        return

    if renderer.get_history_button_collision(pos):
        history.open()


def handle_board_click(pos):
    """Handle clicks on the game board."""
    click_x, click_y = pos

    for field_index, x, y in renderer.hole_positions:
        distance = math.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)

        if distance < HOLE_RADIUS:
            try:
                game.board.seed_from_field(field_index, game.current_player())
                game.end_turn()
            except ValueError:
                pass


def update():
    """Update game state each frame."""
    handle_bot_move()
    session.save_result()


def handle_bot_move():
    """Let bot make a move if it is its turn."""
    if game.mode != GameMode.HUMAN_VS_BOT:
        return

    if game.current_player() != game.player_2:
        return

    move = choose_move(
        game.board,
        game.current_player(),
        bot_search_depth if bot_search_depth else 1,
    )

    if move is not None:
        game.board.seed_from_field(move, game.current_player())
        game.end_turn()


def reset_game():
    """Reset the current game state."""
    global game, bot_search_depth, session, names_set

    game = Game()
    renderer.game = game

    session = GameSession(game)
    bot_search_depth = None
    names_set = False

    history.close()


def render():
    """Render the current frame."""
    if game.mode is None:
        if history.active:
            history.render()
        else:
            renderer.draw_mode_selection()

    elif game.mode == GameMode.HUMAN_VS_BOT and bot_search_depth is None:
        renderer.draw_depth_selection()

    elif not names_set:
        renderer.draw_name_input(game.mode)

    else:
        renderer.draw()


if __name__ == "__main__":
    main()
