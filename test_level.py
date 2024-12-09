from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine


class BulletSpawner(GameObject):
    def __init__(self):
        self.transform = Transform2D(0, 0, 0)
        self.sprite = None
        self.i=1
        self.x=pygame.image.load("Sprites\Enemy Bullet 1.png")

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:
            self.i+=1
            engine.spawn(Bullet(self.transform,self.x,[100,self.i],[1,self.i*17]))
            


def scene() -> Scene:
    new_scene = Scene(Player(), BulletSpawner())
    return new_scene


main(scene())
