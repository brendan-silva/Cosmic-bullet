from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine


class BulletSpawner(GameObject):
    def __init__(self):
        self.transform = Transform2D(0, 0, 0)
        self.sprite = None

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:
            engine.spawn(Bullet(Transform2D(0, 0, 180)))
            print("spawning")


class Bullet(GameObject):
    def __init__(self, transformation: Transform2D):
        self.transform = transformation

        self.sprite = pygame.sprite.Sprite()
        self.sprite.rect = Rect(0, 0, 10, 10)

    def update(self, dt):
        VELOCITY = 200

        self.transform.pos.x += VELOCITY * dt
        self.transform.pos.y += VELOCITY * dt


def scene() -> Scene:
    new_scene = Scene(Player(), BulletSpawner())
    return new_scene


main(scene())
