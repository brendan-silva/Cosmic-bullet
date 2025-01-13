from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine

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
        statusbar(-555,216),
        sidebar(-324,432,"Cosmic-bullet\Sprites\sidebar.png"),
        sidebar(768,432,"Cosmic-bullet\Sprites\sidebar.png")
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
            100,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Cosmic-bullet\Sprites\Enemy Bullet 1.png"),
                    [00, 0],
                    [100, 0],
                    1,
                    0.1,
                    0,
                    [0, 0, 0, 0],
                    [0, 0, 0, 11],
                )
            ],
            10
        ),
        statusbar(-555,216),
        sidebar(-324,432,"Cosmic-bullet\Sprites\sidebar.png"),
        sidebar(768,432,"Cosmic-bullet\Sprites\sidebar.png")
    )
    return new_scene


def main_menu() -> Scene:
    new_scene = Scene(
        #textobject(0,0,"Test",WHITE)
        button(0,0,"stage_2","New Game",False),
        image(0,100,"Cosmic-bullet\Sprites\Player Laser.png")
    )
    return new_scene

def test() -> Scene:
    new_scene = Scene(
        statusbar(-555,216),
        background(-324,432,"Cosmic-bullet\Sprites\sidebar.png"),
        background(768,432,"Cosmic-bullet\Sprites\sidebar.png")
    )
    return new_scene

main('stage_1',lib={'test':test(),'stage_1':stage_1(),'stage_2':stage_2(),'main_menu':main_menu()})
