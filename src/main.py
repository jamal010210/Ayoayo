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
winner_input_active = False
winner_input_text = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and winner_input_active:
            if event.key == pygame.K_BACKSPACE:
                winner_input_text = winner_input_text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                winner_name = winner_input_text.strip() or game.get_winner_name()
                p1_score, p2_score = game.get_scores()
                persistence.save_result(winner_name, p1_score, p2_score)
                print(f"Game saved: Winner {winner_name}, Scores {p1_score}-{p2_score}")
                game_saved = True
                winner_input_active = False
            elif len(event.unicode) == 1 and event.unicode.isprintable():
                winner_input_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN and not winner_input_active:
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
        if game.winner == "draw":
            winner_name = "Draw"
            p1_score, p2_score = game.get_scores()
            persistence.save_result(winner_name, p1_score, p2_score)
            print(f"Game saved: Draw, Scores {p1_score}-{p2_score}")
            game_saved = True
        elif not winner_input_active:
            winner_input_active = True
            winner_input_text = ""

    if mode is None:
        renderer.draw_mode_selection()
    elif mode == "2" and depth is None:
        renderer.draw_depth_selection()
    else:
        renderer.draw()
        if winner_input_active:
            renderer.draw_text_input("Enter winner name:", winner_input_text)
    clock.tick(60)
