from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine

class BulletSpawner(GameObject):
    def __init__(self):
        self.transform = Transform2D(0, 0, 0)
        self.sprite = None
        self.shotcooldown = 0
        self.i = 1
        self.x = pygame.image.load("Cosmic-bullet\Sprites\Enemy Bullet 1.png")

    def update(self, dt):
        if self.shotcooldown >= 0:
            self.shotcooldown -= dt
        if self.shotcooldown <= 0:
            for x in range(0, 360, 30):
                engine.spawn(
                    Bullet(
                        Transform2D(0, 300, 0),
                        self.x,
                        [10, x + self.i],
                        [100, self.i * 141],
                    )
                )
                # engine.spawn(Bullet(Transform2D(0, 300, 0),self.x,[10,x+self.i],[25,self.i*3]))
                # engine.spawn(Bullet(Transform2D(0, 300, 0),self.x,[10,x+self.i],[50,self.i*9]))
            self.shotcooldown += 0.10
            self.i += 1

def stage_1() -> Scene:
    new_scene = Scene(
        Player(),
        enemy(
            Transform2D(0, 300, 0),
            pygame.image.load("Cosmic-bullet/Sprites/Enemy.png"),
            [100, 135],
            [10, -60],
            1,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Cosmic-bullet/Sprites/Enemy Bullet 1.png"),
                    [10, 0],
                    [100, 0],
                    12,
                    0.1,
                    0,
                    [0, 30, 0, 0],
                    [0, 0, 0, 141],
                )
            ],
        ),
    )
    return new_scene


def stage_2() -> Scene:
    new_scene = Scene(
        Player(),
        wavedata(
            Transform2D(0, 300, 0),
            pygame.image.load("Cosmic-bullet\Sprites\Enemy.png"),
            [100, 180],
            [0, 0],
            1,
            0.5,
            2,
            [0,0,0,0],
            [0,10,0,0],
            1,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Cosmic-bullet\Sprites\Enemy Bullet 1.png"),
                    [00, 0],
                    [0, 0],
                    100,
                    0.1,
                    0,
                    [0, 0, 0, 0],
                    [0, 0, 0, 11],
                )
            ],
            10
        ),
    )
    return new_scene


def main_menu() -> Scene:
    new_scene = Scene(
        button(0,0,"test","Test Button")
    )
    return new_scene

main('stage_2',lib={'stage_1':stage_1(),'stage_2':stage_2(),'main_menu':main_menu()})
