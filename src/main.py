import math
import pygame
from game_logic.Game import Game
from Board_renderer import Renderer, HOLE_RADIUS
from bot.bot_logic import choose_move, get_legal_moves
from GameMode import GameMode

# pylint: disable=no-member





pygame.init()
game = Game()
renderer = Renderer(game)
renderer.update_bean_positions()
clock = pygame.time.Clock()
bot_search_depth: int | None = None

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
            else:
                if renderer.get_undo_button_collision(event.pos):
                    previous_round = game.current_round()
                    game.undo_turn()
                    if game.current_round() != previous_round:
                        renderer.update_bean_positions()
                    continue

                click_x, click_y = event.pos
                for field_index, x, y in renderer.hole_positions:
                    distance = math.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)
                    if distance < HOLE_RADIUS:
                        try:
                            game.board.seed_from_field(field_index, game.current_player())
                            game.end_turn()
                            renderer.update_bean_positions()
                        except ValueError:
                            pass


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
                renderer.update_bean_positions()

    if game.mode is None:
        renderer.draw_mode_selection()
    elif game.mode == GameMode.HUMAN_VS_BOT and bot_search_depth is None:
        renderer.draw_depth_selection()
    else:
        renderer.draw()
    clock.tick(60)
