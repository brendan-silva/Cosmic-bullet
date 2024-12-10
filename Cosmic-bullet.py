from tkinter import font
import pygame
from pygame.locals import *
from math import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect(width / 2, 3 / 4 * height, 10, 10)
        self.x = self.rect.x
        self.y = self.rect.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, p, v, A):
        super().__init__()
        self.p = pygame.Vector2(p[0], p[1])
        self.v = pygame.Vector2(v[0], 0)
        self.v = self.v.rotate(v[1])
        self.A = pygame.Vector2(
            A[0],
        )
        self.A = self.A.rotate(A[1])

        self.rect = Rect(self.p.x, self.p.y, 10, 10)
        self.t = 0

    def move(self):
        self.t += 1
        self.p += self.v
        self.v += self.A
        self.rect.y = self.p.y
        self.rect.x = self.p.x


size = 1536, 864
width, height = size
BLACK = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode(size)
running = True
gSpd = 1
p1 = Player()

bullets = pygame.sprite.Group()


t = 0
ang = 0
clock = pygame.time.Clock()
fps = 60
while running:
    clock.tick()
    t += 1
    if t % 50 == 0:
        ang += 11
        for i in range(0, 360, 10):
            bullets.add(
                Bullet([1 / 2 * width, 1 / 4 * height], [1, i + ang], [0.000, ang])
            )

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    if keys.count(True) == 2:
        gSpd = 2
    else:
        gSpd = 3
    if keys[K_w] and p1.rect.top > 0:
        p1.y -= gSpd
    if keys[K_s] and p1.rect.bottom < height:
        p1.y += gSpd
    if keys[K_a] and p1.rect.left > 0:
        p1.x -= gSpd
    if keys[K_d] and p1.rect.right < width:
        p1.x += gSpd

    screen.fill(BLACK)

    for entity in bullets:
        entity.move()

        pygame.draw.rect(screen, RED, entity.rect)
    p1.rect.x = p1.x
    p1.rect.y = p1.y
    pygame.draw.rect(screen, WHITE, p1.rect)
    pygame.display.update()
    clock.tick(fps)


pygame.quit()
