from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine

def stage_1() -> Scene:
    new_scene = Scene(
        Player(),
        bossenemy(
            Transform2D(0, 300, 0),
            pygame.image.load("Sprites/Enemy.png"),
            'stage_2',
            [10,10],
            [
                [
                    shotdata(
                        Transform2D(0, 0, 0),
                        pygame.image.load("Sprites/Enemy Bullet 1.png"),
                        [10, 0],
                        [100, 0],
                        12,
                        0.1,
                        0,
                        [0, 30, 0, 0],
                        [0, 0, 0, 141],
                    )
                ],
                [
                    shotdata(
                        Transform2D(0, 0, 0),
                        pygame.image.load("Sprites/Enemy Bullet 1.png"),
                        [10, 0],
                        [100, 0],
                        12,
                        0.05,
                        0,
                        [0, 30, 0, 0],
                        [0, 0, 0, 141],
                    )
                ]
            ],
        ),
    )
    return new_scene


def stage_2() -> Scene:
    new_scene = Scene(
        Player(),
        wavedata(
            Transform2D(0, 300, 0),
            pygame.image.load("Sprites/Enemy.png"),
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
                    pygame.image.load("Sprites\Enemy Bullet 1.png"),
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

main('stage_1',lib={'stage_1':stage_1(),'stage_2':stage_2(),'main_menu':main_menu()})
