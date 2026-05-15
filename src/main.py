import math
import pygame
from game_logic.Game import Game
from Board_renderer import Renderer, HOLE_RADIUS
import persistence
from bot.bot_logic import choose_move, get_legal_moves
from GameMode import GameMode

# pylint: disable=no-member





pygame.init()
persistence.init_db()
game = Game()
renderer = Renderer(game)
clock = pygame.time.Clock()
bot_search_depth: int | None = None
game_saved = False
names_set = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.mode is None:
                selected_mode = renderer.get_mode_from_position(event.pos)
                if selected_mode is not None:
                    game.mode = selected_mode
            elif game.mode == GameMode.HUMAN_VS_BOT and bot_search_depth is None:
                bot_search_depth = renderer.get_depth_from_position(event.pos) or bot_search_depth
            elif not names_set:
                renderer.handle_name_input_click(event.pos, game.mode)
            else:
                if renderer.get_return_to_menu_button_collision(event.pos):
                    game = Game()
                    renderer.game = game
                    bot_search_depth = None
                    continue

                if renderer.get_undo_button_collision(event.pos):
                    previous_round = game.current_round()
                    game.undo_turn()
                    continue

                click_x, click_y = event.pos
                for field_index, x, y in renderer.hole_positions:
                    distance = math.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)
                    if distance < HOLE_RADIUS:
                        try:
                            game.board.seed_from_field(field_index, game.current_player())
                            game.end_turn()
                        except ValueError:
                            pass
        if event.type == pygame.KEYDOWN and not names_set:
            if renderer.handle_name_input_key(event, game.mode):
                player1_name, player2_name = renderer.get_player_names()
                if game.mode == GameMode.HUMAN_VS_HUMAN:
                    game.set_player_names(player1_name, player2_name)
                else:  # game.mode == GameMode.HUMAN_VS_BOT
                    game.set_player_names(player1_name, "Bot")
                names_set = True


    if game.mode == GameMode.HUMAN_VS_BOT:
        if game.current_player() == game.player_2:

            move = choose_move(
                game.board,
                game.current_player(),
                get_legal_moves,
                bot_search_depth if bot_search_depth else 1
            )
            if move is not None:
                game.board.seed_from_field(move, game.current_player())
                game.end_turn()

    if game.winner and not game_saved:
        winner_name = game.get_winner_name()
        loser_name = game.get_loser_name()
        p1_score, p2_score = game.get_scores()
        persistence.save_result(winner_name, loser_name, p1_score, p2_score)
        print(f"Game saved: Winner {winner_name}, Loser {loser_name}, Scores {p1_score}-{p2_score}")
        game_saved = True

    if game.mode is None:
        renderer.draw_mode_selection()
    elif game.mode == GameMode.HUMAN_VS_BOT and bot_search_depth is None:
        renderer.draw_depth_selection()
    elif not names_set:
        renderer.draw_name_input(game.mode)
    else:
        renderer.draw()
    clock.tick(60)
