import pygame
import os

#display
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
BOARDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#attributes
SPACESHIP_W, SPACESHIP_H = 55, 40
FPS = 60
VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#assets
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_W, SPACESHIP_H)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_RED.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_W, SPACESHIP_H)), 270)


def draw_window(red, yellow, red_bullets, yellow_bullets):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, BOARDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow, speed_yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL * speed_yellow
    if keys_pressed[pygame.K_d] and yellow.x + VEL + SPACESHIP_W < BOARDER.x:  # right
        yellow.x += VEL * speed_yellow
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL * speed_yellow
    if keys_pressed[pygame.K_s] and yellow.y + VEL + SPACESHIP_H < HEIGHT - 15:  # down
        yellow.y += VEL * speed_yellow


def red_handle_movement(keys_pressed, red, speed_red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BOARDER.x + BOARDER.width:  # left
        red.x -= VEL * speed_red
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL * speed_red
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL * speed_red
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + SPACESHIP_H < HEIGHT - 15:  # down
        red.y += VEL * speed_red


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_H, SPACESHIP_W)
    red = pygame.Rect(700, 300, SPACESHIP_H, SPACESHIP_W)
    speed_yellow = 1
    speed_red = 1

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, speed_yellow)
        red_handle_movement(keys_pressed, red, speed_red)


        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets)

    pygame.quit()


if __name__ == '__main__':
    main()
