import math
import pygame
from game_logic.Game import Game
from Board_renderer import Renderer, HOLE_RADIUS
from bot.bot_logic import choose_move, get_legal_moves

# pylint: disable=no-member



pygame.init()
game = Game()
renderer = Renderer(game)
renderer.update_bean_positions()
clock = pygame.time.Clock()
mode = input("Choose mode: 1 = Human vs Human, 2 = Human vs Bot: ")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
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
                get_legal_moves
            )
            if move is not None:
                game.board.seed_from_field(move, game.current_player())
                game.end_turn()
                
    renderer.draw()
    clock.tick(60)
