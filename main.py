import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

FONT = pygame.font.SysFont("comicsans", 30)
SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT = 60, 55

FPS = 60
VEL = 5

VIOLET_SPACECRAFT_IMG = pygame.image.load("./Assets/spaceship_violet.png")
RED_SPACECRAFT_IMG = pygame.image.load("./Assets/spaceship_red.png")


VIOLET_SPACECRAFT_TRANSFORM = pygame.transform.rotate(
    pygame.transform.scale(
        VIOLET_SPACECRAFT_IMG, (SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT)
    ),
    (270),
)
RED_SPACECRAFT_TRANSFORM = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACECRAFT_IMG, (SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT)),
    (90),
)

pygame.display.set_caption("Galaxy Fighter")


def drawWindows(VIOLET_SPACECRAFT, RED_SPACECRAFT):
    WIN.fill("white")

    WIN.blit(VIOLET_SPACECRAFT_TRANSFORM, (VIOLET_SPACECRAFT.x, VIOLET_SPACECRAFT.y))
    WIN.blit(RED_SPACECRAFT_TRANSFORM, (RED_SPACECRAFT.x, RED_SPACECRAFT.y))

    pygame.draw.rect(WIN, "black", BORDER)
    pygame.display.update()


def keyBehaviour(keys, VIOLET_SPACECRAFT, RED_SPACECRAFT):

    if keys[pygame.K_a] and RED_SPACECRAFT.x - VEL > 0:
        RED_SPACECRAFT.x -= VEL
    if keys[pygame.K_d] and RED_SPACECRAFT.x + VEL + RED_SPACECRAFT.width < BORDER.x:
        RED_SPACECRAFT.x += VEL
    if keys[pygame.K_w] and RED_SPACECRAFT.y - VEL > 0:
        RED_SPACECRAFT.y -= VEL
    if keys[pygame.K_s] and RED_SPACECRAFT.y + VEL + RED_SPACECRAFT.height < HEIGHT:
        RED_SPACECRAFT.y += VEL

    if keys[pygame.K_LEFT] and RED_SPACECRAFT.x - VEL > 0:
        VIOLET_SPACECRAFT.x -= VEL
    if keys[pygame.K_RIGHT] and RED_SPACECRAFT.x + VEL + RED_SPACECRAFT.width < BORDER.x :
        VIOLET_SPACECRAFT.x += VEL
    if keys[pygame.K_UP] and RED_SPACECRAFT.y - VEL > BORDER.x + BORDER.width:
        VIOLET_SPACECRAFT.y -= VEL
    if keys[pygame.K_DOWN] and RED_SPACECRAFT.y + VEL + RED_SPACECRAFT.height < HEIGHT:
        VIOLET_SPACECRAFT.y += VEL


def main():

    VIOLET_SPACECRAFT = pygame.Rect(750, 350, SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT)
    RED_SPACECRAFT = pygame.Rect(250, 350, SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] or keys[pygame.K_LCTRL] and keys[pygame.K_w]:

            run = False

        # ------------------------------- keyBehaviour ------------------------------- #

        keyBehaviour(keys, VIOLET_SPACECRAFT, RED_SPACECRAFT)

        if BORDER.collidepoint(
            VIOLET_SPACECRAFT.x, VIOLET_SPACECRAFT.y
        ) or BORDER.collidepoint(RED_SPACECRAFT.x + 50, RED_SPACECRAFT.y):
            run = False

        # -------------------------------- drawWindows ------------------------------- #

        drawWindows(VIOLET_SPACECRAFT, RED_SPACECRAFT)

    pygame.quit()


if __name__ == "__main__":
    main()
