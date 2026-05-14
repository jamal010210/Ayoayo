import math
import pygame
from game_logic.Game import Game
from Board_renderer import Renderer, HOLE_RADIUS
import persistence
from bot.bot_logic import choose_move, get_legal_moves

# pylint: disable=no-member



pygame.init()
persistence.init_db()
game = Game()
renderer = Renderer(game)
renderer.update_bean_positions()
clock = pygame.time.Clock()
mode = None
depth = None
game_saved = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode is None:
                mode = renderer.get_mode_from_position(event.pos) or mode
            elif mode == "2" and depth is None:
                depth = renderer.get_depth_from_position(event.pos) or depth
            else:
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

    if mode == "2":
        if game.current_player() == game.player_2:

            move = choose_move(
                game.board,
                game.current_player(),
                get_legal_moves,
                int(depth) if depth else 1
            )
            if move is not None:
                game.board.seed_from_field(move, game.current_player())
                game.end_turn()
                renderer.update_bean_positions()

    if game.winner and not game_saved:
        winner_name = game.get_winner_name()
        p1_score, p2_score = game.get_scores()
        persistence.save_result(winner_name, p1_score, p2_score)
        print(f"Game saved: Winner {winner_name}, Scores {p1_score}-{p2_score}")
        game_saved = True
                
    if mode is None:
        renderer.draw_mode_selection()
    elif mode == "2" and depth is None:
        renderer.draw_depth_selection()
    else:
        renderer.draw()
    clock.tick(60)
