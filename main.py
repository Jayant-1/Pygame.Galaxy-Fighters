import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont("comicsans", 30)

FPS = 60

VIOLET_SPACECRAFT_IMG = pygame.image.load("./Assets/spaceship_violet.png")
RED_SPACECRAFT_IMG = pygame.image.load("./Assets/spaceship_violet.png")

pygame.display.set_caption("Galaxy Fighter")


def drawWindows():
    WIN.fill()
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    score = 0

    while run:
        clock.tick(FPS)
        WIN.fill("White")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] or keys[pygame.K_LCTRL] and keys[pygame.K_w]:

            run = False

    pygame.quit()


if __name__ == "__main__":
    main()
