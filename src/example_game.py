"""
A very basic test for pygame
"""

import os

import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
board_img = pygame.image.load(
    os.path.join(ASSETS_DIR, "board_test.png")
).convert()
board_img = pygame.transform.scale(
    board_img, (board_img.get_width() * 0.5, board_img.get_height() * 0.5)
)

board_img.set_colorkey((0, 0, 0))

running = True
x = 0

clock = pygame.time.Clock()

delta_time = 0.1

while running:
    screen.fill((255, 255, 255))
    screen.blit(board_img, (100, 200))
    screen.blit(board_img, (x, 30))

    mpos = pygame.mouse.get_pos()

    x += 50 * delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()
