import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 8, HEIGHT)

FONT = pygame.font.SysFont("comicsans", 80)
FONT1 = pygame.font.SysFont("comicsans", 30)
SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT = 60, 55

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 6

BULLET_HIT_SOUND = pygame.mixer.Sound("./Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("./Assets/Gun+Silencer.mp3")

BULLET = []

VIOLET_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

VIOLET_SPACECRAFT_IMG = pygame.image.load("./Assets/spaceship_violet.png")
RED_SPACECRAFT_IMG = pygame.image.load("./Assets/spaceship_red.png")

BG = pygame.transform.scale(pygame.image.load("./Assets/space.png"), (WIDTH, HEIGHT))

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


def drawWindows(
    VIOLET_SPACECRAFT,
    RED_SPACECRAFT,
    red_bullets,
    violet_bullets,
    red_health,
    violet_health,
):
    WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, "black", BORDER)

    WIN.blit(VIOLET_SPACECRAFT_TRANSFORM, (VIOLET_SPACECRAFT.x, VIOLET_SPACECRAFT.y))
    WIN.blit(RED_SPACECRAFT_TRANSFORM, (RED_SPACECRAFT.x, RED_SPACECRAFT.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, "red", bullet)

    for bullet in violet_bullets:
        pygame.draw.rect(WIN, "blue", bullet)

    red_health_text = FONT1.render("Health: " + str(red_health), 1, "White")
    violet_health_text = FONT1.render("Health: " + str(violet_health), 1, "White")
    WIN.blit(
        red_health_text,
        (
            WIDTH - red_health_text.get_width() - 20,
            HEIGHT - violet_health_text.get_height() - 10,
        ),
    )
    WIN.blit(violet_health_text, (5, HEIGHT - red_health_text.get_height() - 10))

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

    if keys[pygame.K_LEFT] and VIOLET_SPACECRAFT.x - VEL > BORDER.x + BORDER.width:
        VIOLET_SPACECRAFT.x -= VEL
    if (
        keys[pygame.K_RIGHT]
        and VIOLET_SPACECRAFT.x + VEL + VIOLET_SPACECRAFT.width < WIDTH
    ):
        VIOLET_SPACECRAFT.x += VEL
    if keys[pygame.K_UP] and VIOLET_SPACECRAFT.y - VEL > 0:
        VIOLET_SPACECRAFT.y -= VEL
    if (
        keys[pygame.K_DOWN]
        and VIOLET_SPACECRAFT.y + VEL + VIOLET_SPACECRAFT.height < HEIGHT
    ):
        VIOLET_SPACECRAFT.y += VEL


def bulletMovement(violet_bullets, red_bullets, VIOLET_SPACECRAFT, RED_SPACECRAFT):

    for bullet in violet_bullets:
        bullet.x -= BULLET_VEL
        if RED_SPACECRAFT.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            violet_bullets.remove(bullet)
        elif bullet.x < 0:
            violet_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if VIOLET_SPACECRAFT.colliderect(bullet):
            pygame.event.post(pygame.event.Event(VIOLET_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)


def main():

    VIOLET_SPACECRAFT = pygame.Rect(750, 350, SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT)
    RED_SPACECRAFT = pygame.Rect(250, 350, SPACECRAFT_WIDTH, SPACECRAFT_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    score = 0

    violet_bullets = []
    red_bullets = []

    violet_health = int(100)
    red_health = int(100)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(violet_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        VIOLET_SPACECRAFT.x,
                        VIOLET_SPACECRAFT.y + VIOLET_SPACECRAFT.height / 2,
                        10,
                        5,
                    )
                    violet_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        RED_SPACECRAFT.x + RED_SPACECRAFT.width,
                        RED_SPACECRAFT.y + RED_SPACECRAFT.height / 2,
                        10,
                        5,
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if red_health <= 0 and violet_health <= 0:
                lost = FONT.render("Draw!", 1, "white")
                WIN.blit(
                    lost,
                    (
                        WIDTH / 2 - lost.get_width() / 2,
                        HEIGHT / 4 - lost.get_height() / 2,
                    ),
                )
                pygame.display.update()
                pygame.time.delay(3000)
                run = False
            if event.type == VIOLET_HIT:
                red_health -= 25
                BULLET_HIT_SOUND.play()
                if red_health <= 0:
                    lost = FONT.render("Red Wins!", 1, "red")
                    WIN.blit(
                        lost,
                        (
                            WIDTH / 2 - lost.get_width() / 2,
                            HEIGHT / 4 - lost.get_height() / 2,
                        ),
                    )
                    pygame.display.update()
                    pygame.time.delay(3000)
                    run = False
                print("Violet Got Hit ", red_health)

            if event.type == RED_HIT:
                violet_health -= 25
                BULLET_HIT_SOUND.play()
                if violet_health <= 0:
                    lost = FONT.render("Blue Wins!", 1, "Blue")
                    WIN.blit(
                        lost,
                        (
                            WIDTH / 2 - lost.get_width() / 2,
                            HEIGHT / 4 - lost.get_height() / 2,
                        ),
                    )
                    pygame.display.update()
                    pygame.time.delay(3000)
                    run = False

                print("Red Got Hit ", violet_health)

        pygame.display.update()

        keys = pygame.key.get_pressed()

        if (
            keys[pygame.K_ESCAPE]
            or BORDER.collidepoint(VIOLET_SPACECRAFT.x, VIOLET_SPACECRAFT.y)
            or BORDER.collidepoint(RED_SPACECRAFT.x + 50, RED_SPACECRAFT.y)
        ):
            run = False

        # ------------------------------- keyBehaviour ------------------------------- #

        keyBehaviour(keys, VIOLET_SPACECRAFT, RED_SPACECRAFT)

        # -------------------------------- drawWindows ------------------------------- #

        drawWindows(
            VIOLET_SPACECRAFT,
            RED_SPACECRAFT,
            red_bullets,
            violet_bullets,
            red_health,
            violet_health,
        )

        # -------------------------------- BulletsPhysics ------------------------------ #

        bulletMovement(violet_bullets, red_bullets, VIOLET_SPACECRAFT, RED_SPACECRAFT)

    pygame.quit()


if __name__ == "__main__":
    main()
