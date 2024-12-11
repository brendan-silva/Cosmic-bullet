from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine



def scene() -> Scene:
    new_scene = Scene(
        Player(),
        enemy(
            Transform2D(0, 300, 0),
            pygame.image.load("Cosmic-bullet\Sprites\Enemy.png"),
            [100, 135],
            [10, -60],
            10,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Cosmic-bullet\Sprites\Enemy Bullet 1.png"),
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


main(scene())
