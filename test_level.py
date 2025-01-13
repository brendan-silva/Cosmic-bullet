from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine

def stage_1() -> Scene:
    new_scene = Scene(
        Player(),
        BarWithText((255, 0, 0), (255, 255, 255), 100, 100, 300, 30, 550, 400, 450, 400, 72),
        bossSpawner(
        bossenemy(
            Transform2D(0, 300, 0),
            pygame.image.load("Sprites/Enemy.png"),
            'stage_2',
            [10,10],
            [1,10],
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
            [[111,111,111,100],[111,111,111,100]]
        ),
        10,
        5,
        ),
        statusbar(-555,216),
        sidebar(-324,432,"Sprites\sidebar.png"),
        sidebar(768,432,"Sprites\sidebar.png")
    )
    return new_scene


def stage_2() -> Scene:
    new_scene = Scene(
        Player(),
        wavedata(
            Transform2D(0, 300, 0),
            pygame.image.load("Sprites/Enemy.png"),
            [10, 180],
            [0, 0],
            1,
            0.5,
            2,
            [0,0,0,0],
            [0,10,0,0],
            100,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Sprites\Enemy Bullet 1.png"),
                    [40, 0],
                    [0, 0],
                    10,
                    0.1,
                    0,
                    [0, 36, 0, 0],
                    [0, 7, 0, 0],
                )
            ],
            1000,
            [111,111,111,100]
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
            [0,72,0,0],
            5,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Sprites\Enemy Bullet 1.png"),
                    [100, 0],
                    [0, 0],
                    1,
                    0.1,
                    0,
                    [0, 0, 0, 0],
                    [0, 11, 0, 0],
                )
            ],
            100
        ),
        statusbar(-555,216),
        sidebar(-324,432,"Sprites\sidebar.png"),
        sidebar(768,432,"Sprites\sidebar.png")
    )
    return new_scene


def test() -> Scene:
    new_scene = Scene(
        statusbar(-555,216),
        background(-324,432,"Sprites\sidebar.png"),
        background(768,432,"Sprites\sidebar.png")
    )
    return new_scene

main('stage_1',lib={'test':test(),'stage_1':stage_1(),'stage_2':stage_2(),'main_menu':main_menu()})
